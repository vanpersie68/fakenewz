# pip install googletrans==3.1.0a0
import argparse
import json
from googletrans import Translator

translator = Translator()
parser = argparse.ArgumentParser()
parser.add_argument('--language', '-l', type=str)
parser.add_argument('--in_filepath', '-fi', type=str)
parser.add_argument('--out_filepath', '-fo', type=str)
args = parser.parse_args()


def trans_json(la: str, in_file_path: str, out_file_path: str):
    f = open(in_file_path, 'r', encoding='utf-8')
    json_contents = json.load(f)
    lang = la if la != 'zh' else 'zh-cn'
    trans_out, retry, retry_cnt = {}, {}, 0
    for global_key in json_contents:
        trans_out[global_key] = {}
        retry[global_key] = {}
        kv_pairs = json_contents[global_key]
        for k, v in kv_pairs.items():
            print(f'{k}: {v}')
            try:
                res = translator.translate(v, src='en', dest=lang).text
                trans_out[global_key][k] = res
            except:
                retry_cnt += 1
                retry[global_key][k] = v
    still_retry = True
    while still_retry:
        rere = {}
        still_retry = False
        print(retry_cnt)
        retry_cnt = 0
        for global_key in retry:
            rere[global_key] = {}
            kv_pairs = retry[global_key]
            for k, v in kv_pairs.items():
                print(f'{k}: {v}')
                try:
                    res = translator.translate(v, src='en', dest=lang).text
                    trans_out[global_key][k] = res
                except:
                    retry_cnt += 1
                    still_retry = True
                    rere[global_key][k] = v
        retry = rere

    with open(out_file_path, 'w', encoding='utf-8') as fo:
        json.dump(trans_out, fo, indent=2, ensure_ascii=False)
    return


if __name__ == '__main__':
    trans_json(args.language, args.in_filepath, args.out_filepath)
