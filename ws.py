from pydub import AudioSegment, effects
import asyncio, websockets, json, time, base64, soundfile, ffmpeg, copy
from io import BytesIO
import torch
import zipfile
import torchaudio
from glob import glob
from pydub import AudioSegment
from utils import Decoder,read_batch, split_into_batches, read_audio, prepare_model_input
labels=['_', 'th', 'the', 'in', 'an', 're', 'er', 'on', 'at', 'ou', 'is', 'en', 'to', 'and', 'ed', 'al', 'as', 'it', 'ing', 'or', 'of', 'es', 'ar', 'he', 'le', 'st', 'se', 'om', 'ic', 'be', 'we', 'ly', 'that', 'no', 'wh', 've', 'ha', 'you', 'ch', 'ion', 'il', 'ent', 'ro', 'me', 'id', 'ac', 'gh', 'for', 'was', 'lo', 'ver', 'ut', 'li', 'ld', 'ay', 'ad', 'so', 'ir', 'im', 'un', 'wi', 'ter', 'are', 'with', 'ke', 'ge', 'do', 'ur', 'all', 'ce', 'ab', 'mo', 'go', 'pe', 'ne', 'this', 'ri', 'ght', 'de', 'one', 'us', 'am', 'out', 'fe', 'but', 'po', 'his', 'te', 'ho', 'ther', 'not', 'con', 'com', 'll', 'they', 'if', 'ould', 'su', 'have', 'ct', 'ain', 'our', 'ation', 'fr', 'ill', 'now', 'sa', 'had', 'tr', 'her', 'per', 'ant', 'oun', 'my', 'ul', 'ca', 'by', 'what', 'red', 'res', 'od', 'ome', 'ess', 'man', 'ex', 'she', 'pl', 'co', 'wor', 'pro', 'up', 'thing', 'there', 'ple', 'ag', 'can', 'qu', 'art', 'ally', 'ok', 'from', 'ust', 'very', 'sh', 'ind', 'est', 'some', 'ate', 'wn', 'ti', 'fo', 'ard', 'ap', 'him', 'were', 'ich', 'here', 'bo', 'ity', 'um', 'ive', 'ous', 'way', 'end', 'ig', 'pr', 'which', 'ma', 'ist', 'them', 'like', 'who', 'ers', 'when', 'act', 'use', 'about', 'ound', 'gr', 'et', 'ide', 'ight', 'ast', 'king', 'would', 'ci', 'their', 'other', 'see', 'ment', 'ong', 'wo', 'ven', 'know', 'how', 'said', 'ine', 'ure', 'more', 'der', 'sel', 'br', 'ren', 'ack', 'ol', 'ta', 'low', 'ough', 'then', 'peo', 'ye', 'ace', 'people', 'ink', 'ort', 'your', 'will', 'than', 'pp', 'any', 'ish', 'look', 'la', 'just', 'tor', 'ice', 'itt', 'af', 'these', 'sp', 'has', 'gre', 'been', 'ty', 'ies', 'ie', 'get', 'able', 'day', 'could', 'bl', 'two', 'time', 'beca', 'into', 'age', 'ans', 'mis', 'new', 'ree', 'ble', 'ite', 'si', 'urn', 'ass', 'cl', 'ber', 'str', 'think', 'dis', 'mar', 'ence', 'pt', 'self', 'ated', 'did', 'el', 'don', 'ck', 'ph', 'ars', 'ach', 'fore', 'its', 'part', 'ang', 'cre', 'well', 'ions', 'where', 'ves', 'ved', 'em', 'good', 'because', 'over', 'ud', 'ts', 'off', 'turn', 'cr', 'right', 'ress', 'most', 'every', 'pre', 'fa', 'fir', 'ild', 'pos', 'down', 'work', 'ade', 'say', 'med', 'also', 'litt', 'little', 'ance', 'come', 'ving', 'only', 'ful', 'ought', 'want', 'going', 'spe', 'ps', 'ater', 'first', 'after', 'ue', 'ose', 'mu', 'iz', 'ire', 'int', 'rest', 'ser', 'coun', 'des', 'light', 'son', 'let', 'ical', 'ick', 'ra', 'back', 'mon', 'ase', 'ign', 'ep', 'world', 'may', 'read', 'form', 'much', 'even', 'should', 'again', 'make', 'long', 'sto', 'cont', 'put', 'thr', 'under', 'cor', 'bet', 'jo', 'car', 'ile', 'went', 'yes', 'ually', 'row', 'hand', 'ak', 'call', 'ary', 'ia', 'many', 'cho', 'things', 'try', 'gl', 'ens', 'really', 'happ', 'great', 'dif', 'bu', 'hi', 'made', 'room', 'ange', 'cent', 'ious', 'je', 'three', 'ward', 'op', 'gen', 'those', 'life', 'tal', 'pa', 'through', 'und', 'cess', 'before', 'du', 'side', 'need', 'less', 'inter', 'ting', 'ry', 'ise', 'na', 'men', 'ave', 'fl', 'ction', 'pres', 'old', 'something', 'miss', 'never', 'got', 'feren', 'imp', 'sy', 'ations', 'tain', 'ning', 'ked', 'sm', 'take', 'ten', 'ted', 'ip', 'col', 'own', 'stand', 'add', 
'min', 'wer', 'ms', 'ces', 'gu', 'land', 'bod', 'log', 'cour', 'ob', 'vo', 'ition', 'hu', 'came', 'comp', 'cur', 'being', 'comm', 'years', 'ily', 'wom', 'cer', 'kind', 'thought', 'such', 'tell', 'child', 'nor', 'bro', 'ial', 'pu', 'does', 'head', 'clo', 'ear', 'led', 'llow', 'ste', 'ness', 'too', 'start', 'mor', 'used', 'par', 'play', 'ents', 'tri', 'upon', 'tim', 'num', 'ds', 'ever', 'cle', 'ef', 'wr', 'vis', 'ian', 'sur', 'same', 'might', 'fin', 'differen', 'sho', 'why', 'body', 'mat', 'beg', 'vers', 'ouse', 'actually', 'ft', 'ath', 'hel', 'sha', 'ating', 'ual', 'found', 'ways', 'must', 'four', 'gi', 'val', 'di', 'tre', 'still', 'tory', 'ates', 'high', 'set', 'care', 'ced', 'last', 'find', 'au', 'inte', 'ev', 'ger', 
'thank', 'ss', 'ict', 'ton', 'cal', 'nat', 'les', 'bed', 'away', 'place', 'house', 'che', 'ject', 'sol', 'another', 'ited', 'att', 'face', 'show', 'ner', 'ken', 'far', 'ys', 'lect', 
'lie', 'tem', 'ened', 'night', 'while', 'looking', 'ah', 'wal', 'dr', 'real', 'cha', 'exp', 'war', 'five', 'pol', 'fri', 'wa', 'cy', 'fect', 'xt', 'left', 'give', 'soci', 'cond', 'char', 'bor', 'point', 'number', 'mister', 'called', 'six', 'bre', 'vi', 'without', 'person', 'air', 'different', 'lot', 'bit', 'pass', 'ular', 'youn', 'won', 'main', 'cri', 'ings', 'den', 'water', 'human', 'around', 'quest', 'ters', 'ities', 'feel', 'each', 'friend', 'sub', 'though', 'saw', 'ks', 'hund', 'hundred', 'times', 'lar', 'ff', 'amer', 'scho', 'sci', 'ors', 'lt', 'arch', 'fact', 'hal', 'himself', 'gener', 'mean', 'vol', 'school', 'ason', 'fam', 'ult', 'mind', 'itch', 'ped', 'home', 'young', 'took', 'big', 'love', 'reg', 'eng', 'sure', 'vent', 'ls', 'ot', 'ince', 'thous', 'eight', 'thousand', 'better', 'mom', 'appe', 'once', 'ied', 'mus', 'stem', 'sing', 'ident', 'als', 'uh', 'mem', 'produ', 'stud', 'power', 'atch', 'bas', 'father', 'av', 'nothing', 'gir', 'pect', 'unt', 'few', 'kes', 'eyes', 'sk', 'always', 'ared', 'toge', 'stru', 'together', 'ics', 'bus', 'fort', 'ween', 'rep', 'ically', 
'small', 'ga', 'mer', 'ned', 'ins', 'between', 'yet', 'stre', 'hard', 'system', 'course', 'year', 'cept', 'publ', 'sim', 'sou', 'ready', 'follow', 'present', 'rel', 'turned', 'sw', 'possi', 'mother', 'io', 'bar', 'ished', 'dec', 'ments', 'pri', 'next', 'ross', 'both', 'ship', 'ures', 'americ', 'eas', 'asked', 'iness', 'serv', 'ists', 'ash', 'uni', 'build', 'phone', 'lau', 'ctor', 'belie', 'change', 'interest', 'peri', 'children', 'thir', 'lear', 'plan', 'import', 'ational', 'har', 'ines', 'dist', 'selves', 'city', 'sen', 'run', 'law', 'ghter', 'proble', 'woman', 'done', 'heart', 'book', 'aut', 'ris', 'lim', 'looked', 'vid', 'fu', 'bab', 'ately', 'ord', 'ket', 'oc', 'doing', 'area', 'tech', 'win', 'name', 'second', 'certain', 'pat', 'lad', 'quite', 'told', 'ific', 'ative', 'uring', 'gg', 'half', 'reason', 'moment', 'ility', 'ution', 'shall', 'aur', 'enough', 'idea', 'open', 'understand', 'vie', 'contin', 'mal', 'hor', 'qui', 'address', 'heard', 'help', 'inst', 'oney', 'whole', 'gover', 'commun', 'exam', 'near', 'didn', 'logy', 'oh', 'tru', 'lang', 'restaur', 'restaurant', 'design', 'ze', 'talk', 'leg', 'line', 'ank', 'ond', 'country', 'ute', 'howe', 'hold', 'live', 'comple', 'however', 'ized', 'ush', 'seen', 'bye', 'fer', 'ital', 'women', 'net', 'state', 
'bur', 'fac', 'whe', 'important', 'dar', 'nine', 'sat', 'fic', 'known', 'having', 'against', 'soon', 'ety', 'langu', 'public', 'sil', 'best', 'az', 'knew', 'black', 'velo', 'sort', 'seven', 'imag', 'lead', 'cap', 'ask', 'alth', 'ature', 'nam', 'began', 'white', 'sent', 'sound', 'vir', 'days', 'anything', 'yeah', 'ub', 'blo', 'sun', 'story', 'dire', 'money', 'trans', 'mil', 'org', 'grow', 'cord', 'pped', 'cus', 'spo', 'sign', 'beaut', 'goodbye', 'inde', 'large', 'question', 'often', 'hour', 'que', 'pur', 'town', 'ield', 'coming', 'door', 'lig', 'ling', 'incl', 'partic', 'keep', 'engl', 'move', 'later', 'ants', 'food', 'lights', 'bal', 'words', 'list', 'aw', 'allow', 'aren', 'pret', 'tern', 'today', 'believe', 'almost', 
'bir', 'word', 'possible', 'ither', 'case', 'ried', 'ural', 'round', 'twent', 'develo', 'plain', 'ended', 'iting', 'chang', 'sc', 'boy', 'gy', 'since', 'ones', 'suc', 'cas', 'national', 'plac', 'teen', 'pose', 'started', 'mas', 'fi', 'fif', 'afr', 'fully', 'grou', 'wards', 'girl', 'e', 't', 'a', 'o', 'i', 'n', 's', 'h', 'r', 'l', 'd', 'u', 'c', 'm', 'w', 'f', 'g', 'y', 'p', 'b', 'v', 'k', "'", 'x', 'j', 'q', 'z', '-', '2', ' ']
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = torch.jit.load("model/en_v6.jit").cuda()
decoder = Decoder(labels)
rdir = "/recordings/"

book = open("frankenstein.txt", "r",  encoding="utf8").readlines()
async def handle_conn(websocket, path):
    print(f"connected {websocket.remote_address}")
    jsonObj={}
    while True:
        data = await websocket.recv()
        data = json.loads(data)
        if data["action"] == "processVoice":
            print("processing")
            data["audioData"] = await websocket.recv()
            rec_time = time.strftime("%d_%m__%Y_%H_%M_%S")
            jsonObj = processVoice(data, rec_time)
            dump = json.dumps(jsonObj)
        else:
            dump = json.dumps({"bookline":book[0]})
        await websocket.send(dump)

def processVoice(data, rec_time, ip):
    
    if isinstance(data["audioData"], str):
        ext = "m4a"
        fname = f"{rdir}{str(ip).replace('.','-')}_{rec_time}.{ext}"
        f = open(fname,"wb")
        f.write(base64.b64decode(data["audioData"]))
        f.close()
    else:
        ext="webm"
        fname = f"{rdir}{str(ip).replace('.','-')}_{rec_time}.{ext}"
        f = open(fname,"wb")
        f.write(data["audioData"])
        f.close()
    a = True
    try:
        if data["browser"] == False:  
            tmp = BytesIO()
            to_wav = AudioSegment.from_file(fname,ext)
            to_wav = effects.normalize(to_wav)
            to_wav.export(fname.replace("webm","wav"), format="wav")   
            #audioD, sample_rate = soundfile.read(copy.deepcopy(tmp))
        else:
            fname = fname.replace(".webm", ".wav")
            (ffmpeg
                .input(fname)
                .output(fname, f="wav", loglevel="quiet", hide_banner="true")
                .overwrite_output()       
                .run())
            #audioD, sample_rate = soundfile.read(tmp)
        batches = split_into_batches([fname], batch_size=10)
        input = prepare_model_input(read_batch(batches[0]),
                            device=device)

        output = model(input)
        recog = ""
        for example in output:
            recog += decoder(example.cpu())
        
    except Exception as e:
        print(f" the error was : {e} ")
        recog = "sorry I didn't catch that"
    
    return {"result":"recog","recog":recog}

start_server = websockets.serve(handle_conn, port=1337)#, ssl=context)
print("starting server on 1337")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
