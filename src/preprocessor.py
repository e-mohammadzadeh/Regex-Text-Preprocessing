import pandas as pd
import regex as re
import json
import os
import string
import pickle
from .config import PreprocessingConfig


# Unicode markers used to protect specific entities (URL, Email, etc.) from being deleted
PROTECTION_START = '\u1405'  # ᐅ
PROTECTION_END = '\u140A'  # ᐊ


class TextPreprocessor:
	def __init__(self, config: PreprocessingConfig):
		self.config = config

		# Storage for mapping replaced entities (e.g., $L1 -> https://google.com)
		self.maps = {
			'urls': {},
			'emails': {},
			'money': {},
			'time': {}
		}

		# Load external resources (Slangs, Contractions)
		self.slang_dict = {}
		self.contraction_dict = {}
		self.stopwords = set()
		self._load_resources()

		# Compile Regex Patterns (Performance Optimization)
		self._compile_patterns()

	def _compile_patterns(self):
		"""Pre-compile regex patterns to speed up processing."""
		# URLs
		self.url_pattern = re.compile(
			r'(http(s)?:\/\/|www\.)[-a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)')

		# Emails
		self.email_pattern = re.compile(r'\b[a-zA-Z0-9.-_]+@[a-zA-Z0-9.-]+\.[a-zA-Z]+\b')

		# Mentions
		self.mention_pattern = re.compile(r'(?<=\s|^)@[A-Za-z0-9_.]+(?=\s|$)')

		# Hashtags
		self.hashtag_pattern = re.compile(r'\#[a-zA-Z0-9_]*[a-zA-Z][a-zA-Z0-9_]*')

		# Tag
		self.html_tag_pattern = re.compile(r'<\/?\w+[^>]*?>')

		# Cashtag
		self.cashtag_pattern = re.compile(r'(?<![A-Z])\$[A-Z]+\b')

		# Titles
		titles_list = ['Mr', 'Ms', 'Mrs', 'Miss', 'Dr', 'Prof', 'Sir', "Ma'am", 'Madam', 'Madame', 'Rev', 'Fr', 'Sr',
		               'Capt', 'Gen', 'Hon', 'Pres']
		self.title_pattern = re.compile(r'|'.join([r'(?i)' + t + r'\.? ' for t in titles_list]))

		# Date
		short_date = r'(?:\b(?<!\d\.)(?:(?:(?:[0123]?[0-9][\.\-\/])?[0123]?[0-9][\.\-\/][12][0-9]{3})|(?:[0123]?[0-9][\.\-\/][0123]?[0-9][\.\-\/][12]?[0-9]{2,3}))(?!\.\d)\b)'
		date_parts = [
			r'(?:(?<!:)\b\d{1,4},? ?)',  # Prefix
			r'\b(?:[Jj]an(?:uary)?|[Ff]eb(?:ruary)?|[Mm]ar(?:ch)?|[Aa]pr(?:il)?|[Mm]ay|[Jj]un(?:e)?|[Jj]ul(?:y)?|[Aa]ug(?:ust)?|[Ss]ept?(?:ember)?|[Oo]ct(?:ober)?|[Nn]ov(?:ember)?|[Dd]ec(?:ember)?)\b',
			# Month names
			r'(?:(?:,? ?)?\d{1,4}(?:st|nd|rd|n?th)?\b(?:[,\/]? ?\d{2,4}[a-zA-Z]*)?(?: ?- ?\d{2,4}[a-zA-Z]*)?(?!:\d{1,4})\b)',
			# Suffix
			r'\s*(?:of \d{4})',  # of YYYY
		]
		fd1 = f"(?:{date_parts[0]}?{date_parts[1]}{date_parts[2]}?{date_parts[3]})"
		fd2 = f"(?:{date_parts[0]}{date_parts[1]}{date_parts[2]}?)"
		fd3 = f"(?:{date_parts[0]}?{date_parts[1]}{date_parts[2]})"
		self.date_pattern = re.compile(rf'(?:(?:{fd1}|{fd2}|{fd3})|{short_date})')  # Date

		# Money
		money_parts = [
			r"[$€£¥₹¢]",  # Symbols
			r"(\d{1,3}(?:[,']\d{3})+|\d+)(?:(?:\.|\,|\')\d+)",  # Numbers
			r"?(?:[MmKkBbTt](?:n|(?:(ill|rill)(?:ion)?))?)?",  # Unit system
		]
		fd1 = money_parts[0] + money_parts[1] + money_parts[2]
		fd2 = money_parts[1] + money_parts[2] + money_parts[0]
		self.money_pattern = re.compile(rf'(?:{fd1})|({fd2})')

		# Time
		time_parts = [
			r"(?:\s?(?:AM|PM|am|pm|A\.M\.|P\.M\.|a\.m\.|p\.m\.))",
			r"(?:\d+)?\.?\d+",  # Short Time Format
			r"(?:[0-2]?[0-9]|[2][0-3]):(?:[0-5][0-9])(?::(?:[0-5][0-9]))?",  # Full Time Format
		]
		self.time_pattern = re.compile(rf'(?:{time_parts[1]}{time_parts[0]})|(?:{time_parts[2]}{time_parts[0]}?)')

		# Repeated letters
		self.repeated_char_pattern = re.compile(r"(\D)\1{2,}")

	def _load_resources(self):
		"""Safely load JSON and TXT resources."""
		# Load Slang words
		if self.config.replace_slang_words:
			path = os.path.join(self.config.resource_dir, 'English_Slang_Dict.json')
			try:
				with open(path, 'r', encoding='utf-8') as f:
					raw_slangs = json.load(f)
					# Pre-format slangs with spaces for regex safety
					self.slang_dict = {f'\\b{re.escape(k)}\\b': f' {v} ' for k, v in raw_slangs.items()}
			except FileNotFoundError:
				print(f"Warning: Slang dictionary not found at {path}")

		# Load Contractions
		if self.config.expand_contractions:
			path = os.path.join(self.config.resource_dir, 'English_Contractions.json')
			try:
				with open(path, 'r', encoding='utf-8') as f:
					self.contraction_dict = json.load(f)
			except FileNotFoundError:
				print(f"Warning: Contraction dictionary not found at {path}")

		# Load Stopwords
		if self.config.remove_stopwords:
			path = os.path.join(self.config.resource_dir, 'English_Stopwords_without_negatives.txt')
			try:
				with open(path, 'r', encoding='utf-8') as f:
					content = f.read()
					# Handle both comma-separated or newline-separated files
					self.stopwords = set(content.replace(',', '\n').split())
			except FileNotFoundError:
				print(f"Warning: Stopwords file not found at {path}")

	def process_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
		"""Main pipeline execution."""
		df = df.copy()

		# Identify text columns automatically
		text_cols = df.select_dtypes(include=['object', 'string']).columns

		# 1. Null Handling
		if self.config.remove_null:
			df.dropna(inplace=True)

		# 2-9. Replace URLs, Emails, Time, Money - Expand Mentions, Hashtags - Remove HTML Tags, Cashtags
		for col in text_cols:
			df[col] = df[col].apply(self._clean_text_before_lowercase)

		# 10. Contractions
		if self.config.expand_contractions and self.contraction_dict:
			df[text_cols] = df[text_cols].replace(self.contraction_dict, regex=True)

		# 11. Slang Replacement
		if self.config.replace_slang_words and self.slang_dict:
			df[text_cols] = df[text_cols].replace(self.slang_dict, regex=True)

		# 12. Lowercase
		if self.config.check_lowercase:
			for col in text_cols:
				df[col] = df[col].astype(str).str.lower()

		# 13-18: Remove Dates, stopwords, Titles, Numbers, Punctuation - Replace Repeated Letters
		for col in text_cols:
			df[col] = df[col].apply(self._clean_text_after_lowercase)

		# Save the dictionaries (URL maps, etc.) to disk
		self._save_maps()

		return df


	def _clean_text_before_lowercase(self, text: str) -> str:
		if not isinstance(text, str):
			return str(text)

		# STEP 2: Replace URLs
		if self.config.replace_url:
			text = self.url_pattern.sub(lambda m: self._store_entity(m, 'urls', 'L'), text)

		# STEP 3: Replace Emails
		if self.config.replace_email:
			text = self.email_pattern.sub(lambda m: self._store_entity(m, 'emails', 'E'), text)

		# STEP 4: Replace Time
		if self.config.replace_time:
			text = self.time_pattern.sub(lambda m: self._store_entity(m, 'time', 'T'), text)

		# STEP 5: Replace Money
		if self.config.replace_money:
			text = self.money_pattern.sub(lambda m: self._store_entity(m, 'money', 'M'), text)

		# STEP 6: Expand Mentions
		if self.config.expand_mention:
			text = self.mention_pattern.sub(lambda m: m.group()[1:].replace('_', ' '), text)

		# STEP 7: Expand Hashtags
		if self.config.expand_hashtag:
			text = self.hashtag_pattern.sub(lambda m: m.group()[1:].replace('_', ' '), text)

		# STEP 8: Remove HTML Tags
		if self.config.remove_tag:
			text = self.html_tag_pattern.sub(' ', text)

		# STEP 9: Remove Cashtags
		if self.config.remove_cash_tag:
			text = self.cashtag_pattern.sub(' ', text)

		return text


	def _clean_text_after_lowercase(self, text: str) -> str:
		if not isinstance(text, str):
			return str(text)

		# STEP 13: Remove Dates
		if self.config.remove_date:
			text = self.date_pattern.sub(' ', text)

		# STEP 14: Remove stopwords
		if self.config.remove_stopwords:
			text = ' '.join([word for word in text.split() if word not in self.stopwords])

		# STEP 15: Remove Titles
		if self.config.remove_titles:
			text = self.title_pattern.sub(' ', text)

		# STEP 16: Remove Numbers (Protected Logic)
		if self.config.remove_number:
			text = self._remove_numbers_logic(text)

		# STEP 17: Remove Punctuation (Protected Logic)
		if self.config.remove_punctuation:
			text = self._remove_punctuation_logic(text)

		# STEP 18: Replace Repeated Letters
		if self.config.replace_repeated_letters:
			text = self.repeated_char_pattern.sub(r'\1\1', text)

		return text

	def _store_entity(self, match, map_name: str, prefix: str) -> str:
		"""Stores a match in the dictionary and returns the marker key."""
		value = match.group(0)
		# Unique ID based on current dictionary size + 1
		current_id = len(self.maps[map_name]) + 1
		key = f"{PROTECTION_START}{prefix}{current_id}{PROTECTION_END}"
		self.maps[map_name][key] = value
		return key

	def _remove_numbers_logic(self, text: str) -> str:
		"""Removes numbers unless they are inside protection markers."""
		# 1. Split text by Unicode markers to separate protected content
		parts = re.split(f"({PROTECTION_START}.*?{PROTECTION_END})", text)
		cleaned_parts = []
		for part in parts:
			if part.startswith(PROTECTION_START) and part.endswith(PROTECTION_END):
				# This is a protected token (e.g., URL placeholder), keep it
				cleaned_parts.append(part)
			else:
				# This is normal text, remove numbers
				cleaned_parts.append(re.sub(r'\d+', '', part))
		return "".join(cleaned_parts)

	def _remove_punctuation_logic(self, text: str) -> str:
		"""Removes punctuation unless inside protection markers."""
		parts = re.split(f"({PROTECTION_START}.*?{PROTECTION_END})", text)
		cleaned_parts = []
		for part in parts:
			if part.startswith(PROTECTION_START) and part.endswith(PROTECTION_END):
				cleaned_parts.append(part)
			else:
				cleaned_parts.append(part.translate(str.maketrans('', '', string.punctuation)))
		return "".join(cleaned_parts)

	def _save_maps(self):
		"""Saves the replacement maps to pickle files."""
		if not os.path.exists(self.config.output_dir):
			os.makedirs(self.config.output_dir)

		for name, data in self.maps.items():
			if data:
				file_path = os.path.join(self.config.output_dir, f'{name}_dictionary.pkl')
				with open(file_path, 'wb') as f:
					pickle.dump(data, f)