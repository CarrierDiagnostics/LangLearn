"""from pydub import AudioSegment
m4a_file = 'Recording2.m4a' 
wav_filename = 'output.mp3'
sound = AudioSegment.from_file(m4a_file, format='m4a')
file_handle = sound.export(wav_filename, format='mp3')"""

import torch
import zipfile
import torchaudio
from glob import glob
from pydub import AudioSegment
import utils
from utils import Decoder,read_batch, split_into_batches, read_audio, prepare_model_input
m4a_file = 'Recording2.m4a' 
wav_filename = 'output.wav'
sound = AudioSegment.from_file(m4a_file, format='m4a')
file_handle = sound.export(wav_filename, format='wav')
labels=['_', 'th', 'the', 'in', 'an', 're', 'er', 'on', 'at', 'ou', 'is', 'en', 'to', 'and', 'ed', 'al', 'as', 'it', 'ing', 'or', 'of', 'es', 'ar', 'he', 'le', 'st', 'se', 'om', 'ic', 'be', 'we', 'ly', 'that', 'no', 'wh', 've', 'ha', 'you', 'ch', 'ion', 'il', 'ent', 'ro', 'me', 'id', 'ac', 'gh', 'for', 'was', 'lo', 'ver', 'ut', 'li', 'ld', 'ay', 'ad', 'so', 'ir', 'im', 'un', 'wi', 'ter', 'are', 'with', 'ke', 'ge', 'do', 'ur', 'all', 'ce', 'ab', 'mo', 'go', 'pe', 'ne', 'this', 'ri', 'ght', 'de', 'one', 'us', 'am', 'out', 'fe', 'but', 'po', 'his', 'te', 'ho', 'ther', 'not', 'con', 'com', 'll', 'they', 'if', 'ould', 'su', 'have', 'ct', 'ain', 'our', 'ation', 'fr', 'ill', 'now', 'sa', 'had', 'tr', 'her', 'per', 'ant', 'oun', 'my', 'ul', 'ca', 'by', 'what', 'red', 'res', 'od', 'ome', 'ess', 'man', 'ex', 'she', 'pl', 'co', 'wor', 'pro', 'up', 'thing', 'there', 'ple', 'ag', 'can', 'qu', 'art', 'ally', 'ok', 'from', 'ust', 'very', 'sh', 'ind', 'est', 'some', 'ate', 'wn', 'ti', 'fo', 'ard', 'ap', 'him', 'were', 'ich', 'here', 'bo', 'ity', 'um', 'ive', 'ous', 'way', 'end', 'ig', 'pr', 'which', 'ma', 'ist', 'them', 'like', 'who', 'ers', 'when', 'act', 'use', 'about', 'ound', 'gr', 'et', 'ide', 'ight', 'ast', 'king', 'would', 'ci', 'their', 'other', 'see', 'ment', 'ong', 'wo', 'ven', 'know', 'how', 'said', 'ine', 'ure', 'more', 'der', 'sel', 'br', 'ren', 'ack', 'ol', 'ta', 'low', 'ough', 'then', 'peo', 'ye', 'ace', 'people', 'ink', 'ort', 'your', 'will', 'than', 'pp', 'any', 'ish', 'look', 'la', 'just', 'tor', 'ice', 'itt', 'af', 'these', 'sp', 'has', 'gre', 'been', 'ty', 'ies', 'ie', 'get', 'able', 'day', 'could', 'bl', 'two', 'time', 'beca', 'into', 'age', 'ans', 'mis', 'new', 'ree', 'ble', 'ite', 'si', 'urn', 'ass', 'cl', 'ber', 'str', 'think', 'dis', 'mar', 'ence', 'pt', 'self', 'ated', 'did', 'el', 'don', 'ck', 'ph', 'ars', 'ach', 'fore', 'its', 'part', 'ang', 'cre', 'well', 'ions', 'where', 'ves', 'ved', 'em', 'good', 'because', 'over', 'ud', 'ts', 'off', 'turn', 'cr', 'right', 'ress', 'most', 'every', 'pre', 'fa', 'fir', 'ild', 'pos', 'down', 'work', 'ade', 'say', 'med', 'also', 'litt', 'little', 'ance', 'come', 'ving', 'only', 'ful', 'ought', 'want', 'going', 'spe', 'ps', 'ater', 'first', 'after', 'ue', 'ose', 'mu', 'iz', 'ire', 'int', 'rest', 'ser', 'coun', 'des', 'light', 'son', 'let', 'ical', 'ick', 'ra', 'back', 'mon', 'ase', 'ign', 'ep', 'world', 'may', 'read', 'form', 'much', 'even', 'should', 'again', 'make', 'long', 'sto', 'cont', 'put', 'thr', 'under', 'cor', 'bet', 'jo', 'car', 'ile', 'went', 'yes', 'ually', 'row', 'hand', 'ak', 'call', 'ary', 'ia', 'many', 'cho', 'things', 'try', 'gl', 'ens', 'really', 'happ', 'great', 'dif', 'bu', 'hi', 'made', 'room', 'ange', 'cent', 'ious', 'je', 'three', 'ward', 'op', 'gen', 'those', 'life', 'tal', 'pa', 'through', 'und', 'cess', 'before', 'du', 'side', 'need', 'less', 'inter', 'ting', 'ry', 'ise', 'na', 'men', 'ave', 'fl', 'ction', 'pres', 'old', 'something', 'miss', 'never', 'got', 'feren', 'imp', 'sy', 'ations', 'tain', 'ning', 'ked', 'sm', 'take', 'ten', 'ted', 'ip', 'col', 'own', 'stand', 'add', 
'min', 'wer', 'ms', 'ces', 'gu', 'land', 'bod', 'log', 'cour', 'ob', 'vo', 'ition', 'hu', 'came', 'comp', 'cur', 'being', 'comm', 'years', 'ily', 'wom', 'cer', 'kind', 'thought', 'such', 'tell', 'child', 'nor', 'bro', 'ial', 'pu', 'does', 'head', 'clo', 'ear', 'led', 'llow', 'ste', 'ness', 'too', 'start', 'mor', 'used', 'par', 'play', 'ents', 'tri', 'upon', 'tim', 'num', 'ds', 'ever', 'cle', 'ef', 'wr', 'vis', 'ian', 'sur', 'same', 'might', 'fin', 'differen', 'sho', 'why', 'body', 'mat', 'beg', 'vers', 'ouse', 'actually', 'ft', 'ath', 'hel', 'sha', 'ating', 'ual', 'found', 'ways', 'must', 'four', 'gi', 'val', 'di', 'tre', 'still', 'tory', 'ates', 'high', 'set', 'care', 'ced', 'last', 'find', 'au', 'inte', 'ev', 'ger', 
'thank', 'ss', 'ict', 'ton', 'cal', 'nat', 'les', 'bed', 'away', 'place', 'house', 'che', 'ject', 'sol', 'another', 'ited', 'att', 'face', 'show', 'ner', 'ken', 'far', 'ys', 'lect', 
'lie', 'tem', 'ened', 'night', 'while', 'looking', 'ah', 'wal', 'dr', 'real', 'cha', 'exp', 'war', 'five', 'pol', 'fri', 'wa', 'cy', 'fect', 'xt', 'left', 'give', 'soci', 'cond', 'char', 'bor', 'point', 'number', 'mister', 'called', 'six', 'bre', 'vi', 'without', 'person', 'air', 'different', 'lot', 'bit', 'pass', 'ular', 'youn', 'won', 'main', 'cri', 'ings', 'den', 'water', 'human', 'around', 'quest', 'ters', 'ities', 'feel', 'each', 'friend', 'sub', 'though', 'saw', 'ks', 'hund', 'hundred', 'times', 'lar', 'ff', 'amer', 'scho', 'sci', 'ors', 'lt', 'arch', 'fact', 'hal', 'himself', 'gener', 'mean', 'vol', 'school', 'ason', 'fam', 'ult', 'mind', 'itch', 'ped', 'home', 'young', 'took', 'big', 'love', 'reg', 'eng', 'sure', 'vent', 'ls', 'ot', 'ince', 'thous', 'eight', 'thousand', 'better', 'mom', 'appe', 'once', 'ied', 'mus', 'stem', 'sing', 'ident', 'als', 'uh', 'mem', 'produ', 'stud', 'power', 'atch', 'bas', 'father', 'av', 'nothing', 'gir', 'pect', 'unt', 'few', 'kes', 'eyes', 'sk', 'always', 'ared', 'toge', 'stru', 'together', 'ics', 'bus', 'fort', 'ween', 'rep', 'ically', 
'small', 'ga', 'mer', 'ned', 'ins', 'between', 'yet', 'stre', 'hard', 'system', 'course', 'year', 'cept', 'publ', 'sim', 'sou', 'ready', 'follow', 'present', 'rel', 'turned', 'sw', 'possi', 'mother', 'io', 'bar', 'ished', 'dec', 'ments', 'pri', 'next', 'ross', 'both', 'ship', 'ures', 'americ', 'eas', 'asked', 'iness', 'serv', 'ists', 'ash', 'uni', 'build', 'phone', 'lau', 'ctor', 'belie', 'change', 'interest', 'peri', 'children', 'thir', 'lear', 'plan', 'import', 'ational', 'har', 'ines', 'dist', 'selves', 'city', 'sen', 'run', 'law', 'ghter', 'proble', 'woman', 'done', 'heart', 'book', 'aut', 'ris', 'lim', 'looked', 'vid', 'fu', 'bab', 'ately', 'ord', 'ket', 'oc', 'doing', 'area', 'tech', 'win', 'name', 'second', 'certain', 'pat', 'lad', 'quite', 'told', 'ific', 'ative', 'uring', 'gg', 'half', 'reason', 'moment', 'ility', 'ution', 'shall', 'aur', 'enough', 'idea', 'open', 'understand', 'vie', 'contin', 'mal', 'hor', 'qui', 'address', 'heard', 'help', 'inst', 'oney', 'whole', 'gover', 'commun', 'exam', 'near', 'didn', 'logy', 'oh', 'tru', 'lang', 'restaur', 'restaurant', 'design', 'ze', 'talk', 'leg', 'line', 'ank', 'ond', 'country', 'ute', 'howe', 'hold', 'live', 'comple', 'however', 'ized', 'ush', 'seen', 'bye', 'fer', 'ital', 'women', 'net', 'state', 
'bur', 'fac', 'whe', 'important', 'dar', 'nine', 'sat', 'fic', 'known', 'having', 'against', 'soon', 'ety', 'langu', 'public', 'sil', 'best', 'az', 'knew', 'black', 'velo', 'sort', 'seven', 'imag', 'lead', 'cap', 'ask', 'alth', 'ature', 'nam', 'began', 'white', 'sent', 'sound', 'vir', 'days', 'anything', 'yeah', 'ub', 'blo', 'sun', 'story', 'dire', 'money', 'trans', 'mil', 'org', 'grow', 'cord', 'pped', 'cus', 'spo', 'sign', 'beaut', 'goodbye', 'inde', 'large', 'question', 'often', 'hour', 'que', 'pur', 'town', 'ield', 'coming', 'door', 'lig', 'ling', 'incl', 'partic', 'keep', 'engl', 'move', 'later', 'ants', 'food', 'lights', 'bal', 'words', 'list', 'aw', 'allow', 'aren', 'pret', 'tern', 'today', 'believe', 'almost', 
'bir', 'word', 'possible', 'ither', 'case', 'ried', 'ural', 'round', 'twent', 'develo', 'plain', 'ended', 'iting', 'chang', 'sc', 'boy', 'gy', 'since', 'ones', 'suc', 'cas', 'national', 'plac', 'teen', 'pose', 'started', 'mas', 'fi', 'fif', 'afr', 'fully', 'grou', 'wards', 'girl', 'e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'l', 'd', 'u', 'c', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', "'", 'x', 'j', 'q', 'z', '-', '2', ' ']
m4a_file = 'Recording.m4a' 
wav_filename = 'output.wav'
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(device)
decoder2 = utils.Decoder(labels)
model = torch.jit.load("model/en_v6.jit").cuda()

test_files = glob('speech_orig.wav')
test_files.append("output.wav")
batches = split_into_batches(test_files, batch_size=10)
input = prepare_model_input(read_batch(batches[0]),
                            device=device)

output = model(input)
for example in output:
    print(decoder2(example.cpu()))
    
    