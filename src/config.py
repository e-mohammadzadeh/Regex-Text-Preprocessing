from dataclasses import dataclass


@dataclass
class PreprocessingConfig:
	remove_null: bool = True
	replace_slang_words: bool = True
	check_lowercase: bool = True
	expand_contractions: bool = True
	remove_stopwords: bool = True
	replace_url: bool = True
	remove_line_feed: bool = True
	replace_email: bool = True
	expand_mention: bool = True
	expand_hashtag: bool = True
	remove_date: bool = True
	replace_money: bool = True
	replace_time: bool = True
	remove_tag: bool = True
	remove_cash_tag: bool = True
	remove_number: bool = True
	remove_titles: bool = True
	remove_punctuation: bool = True
	replace_repeated_letters: bool = True

	# Directories (Use relative paths)
	resource_dir: str = './resources'
	files_dir: str = './data/raw'
	output_dir: str = './data/processed/maps'

	@property
	def who_replaced(self) -> str:
		"""Builds the string of replacement flags dynamically."""
		chars = []
		if self.replace_url:
			chars.append('L')
		if self.replace_email:
			chars.append('E')
		if self.replace_money:
			chars.append('M')
		if self.replace_time:
			chars.append('T')

		return ''.join(chars)