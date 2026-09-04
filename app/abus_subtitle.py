import re


def timeformat_srt(time):
    hours = time // 3600
    minutes = (time - hours * 3600) // 60
    seconds = time - hours * 3600 - minutes * 60
    milliseconds = (time - int(time)) * 1000
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d},{int(milliseconds):03d}"


def timeformat_vtt(time):
    hours = time // 3600
    minutes = (time - hours * 3600) // 60
    seconds = time - hours * 3600 - minutes * 60
    milliseconds = (time - int(time)) * 1000
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{int(milliseconds):03d}"


def write_file(subtitle, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(subtitle)


def get_srt(segments):
    output = ""
    for i, segment in enumerate(segments):
        output += f"{i + 1}\n"
        output += f"{timeformat_srt(segment['start'])} --> {timeformat_srt(segment['end'])}\n"
        if segment['text'].startswith(' '):
            segment['text'] = segment['text'][1:]
        output += f"{segment['text']}\n\n"
    return output


def highlight_word(text, striped, cursor):
    """Underline the next occurrence of `striped` at or after `cursor`.

    Words arrive in the order they were spoken, so a cursor that only ever
    moves forward highlights the repetition the caller actually means
    instead of always hitting the first match like str.replace does.
    Returns the marked-up line and the position to resume searching from.
    """
    if not striped:
        return text, cursor

    # Guard only the edges that can collide with a neighbouring letter;
    # scripts written without spaces (CJK) never match a hard \b.
    head = r'(?<!\w)' if striped[0].isalnum() else ''
    tail = r'(?!\w)' if striped[-1].isalnum() else ''
    pattern = re.compile(head + re.escape(striped) + tail)

    match = pattern.search(text, cursor) or pattern.search(text)
    if match is None:
        index = text.find(striped, cursor)
        if index == -1:
            index = text.find(striped)
        if index == -1:
            return text, cursor
        start, end = index, index + len(striped)
    else:
        start, end = match.span()

    highlighted = f'<font color=\"#0e556a\"><b><u>{striped}</u></b></font>'
    return text[:start] + highlighted + text[end:], end


def get_srt_wordlevel(segments):
    output = ""
    i = 0
    for segment in segments:
        cursor = 0
        for word in segment['words']:
            i += 1
            output += f"{i}\n"
            output += f"{timeformat_srt(word.start)} --> {timeformat_srt(word.end)}\n"
            
            striped = word.word.strip()
            line, cursor = highlight_word(segment['text'], striped, cursor)

            output += f"{line}\n\n"    
    return output


def get_vtt(segments):
    output = "WebVTT\n\n"
    for i, segment in enumerate(segments):
        output += f"{i + 1}\n"
        output += f"{timeformat_vtt(segment['start'])} --> {timeformat_vtt(segment['end'])}\n"
        if segment['text'].startswith(' '):
            segment['text'] = segment['text'][1:]
        output += f"{segment['text']}\n\n"
    return output

def get_vtt_block(segments, start_idx=1):
    output = ""
    for i, segment in enumerate(segments):
        output += f"{i + start_idx}\n"
        output += f"{timeformat_vtt(segment['start'])} --> {timeformat_vtt(segment['end'])}\n"
        if segment['text'].startswith(' '):
            segment['text'] = segment['text'][1:]
        output += f"{segment['text']}\n\n"
    return output




def get_txt(segments):
    output = ""
    for i, segment in enumerate(segments):
        if segment['text'].startswith(' '):
            segment['text'] = segment['text'][1:]
        output += f"{segment['text']}\n"
    return output


def parse_srt(file_path):
    """Reads SRT file and returns as dict"""
    with open(file_path, 'r', encoding='utf-8') as file:
        srt_data = file.read()

    data = []
    blocks = srt_data.split('\n\n')

    for block in blocks:
        if block.strip() != '':
            lines = block.strip().split('\n')
            index = lines[0]
            timestamp = lines[1]
            sentence = ' '.join(lines[2:])

            data.append({
                "index": index,
                "timestamp": timestamp,
                "sentence": sentence
            })
    return data


def parse_vtt(file_path):
    """Reads WebVTT file and returns as dict"""
    with open(file_path, 'r', encoding='utf-8') as file:
        webvtt_data = file.read()

    data = []
    blocks = webvtt_data.split('\n\n')

    for block in blocks:
        if block.strip() != '' and not block.strip().startswith("WebVTT"):
            lines = block.strip().split('\n')
            index = lines[0]
            timestamp = lines[1]
            sentence = ' '.join(lines[2:])

            data.append({
                "index": index,
                "timestamp": timestamp,
                "sentence": sentence
            })

    return data


def get_serialized_srt(dicts):
    output = ""
    for dic in dicts:
        output += f'{dic["index"]}\n'
        output += f'{dic["timestamp"]}\n'
        output += f'{dic["sentence"]}\n\n'
    return output


def get_serialized_vtt(dicts):
    output = "WebVTT\n\n"
    for dic in dicts:
        output += f'{dic["index"]}\n'
        output += f'{dic["timestamp"]}\n'
        output += f'{dic["sentence"]}\n\n'
    return output



import time

def safe_filename(name):
    return f'{name}-{int(time.time())}'
    # from app import _args
    # INVALID_FILENAME_CHARS = r'[<>:"/\\|?*\x00-\x1f]'
    # safe_name = re.sub(INVALID_FILENAME_CHARS, '_', name)
    # if not _args.colab:
    #     return safe_name
    # # Truncate the filename if it exceeds the max_length (20)
    # if len(safe_name) > 20:
    #     file_extension = safe_name.split('.')[-1]
    #     if len(file_extension) + 1 < 20:
    #         truncated_name = safe_name[:20 - len(file_extension) - 1]
    #         safe_name = truncated_name + '.' + file_extension
    #     else:
    #         safe_name = safe_name[:20]
    # return safe_name
