from main import Word, Wordgroup

print('start')

i = 22

wg = Wordgroup()
wg.create_wordgroup(f'wordgroup_test{i}')

wa = Word()
wa.create_word(f'word_test{i}a', wg)
wb = Word()
wb.create_word(f'word_test{i}b', wg)

wg = Wordgroup()
wg.load_wordgroup(f'wordgroup_test{i}')

wa = Word()
wa.load_word(f'word_test{i}a')
wb = Word()
wb.load_word(f'word_test{i}b')

wg.load_words()
print(wg.words)

print('end')
