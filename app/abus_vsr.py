import os
import subprocess
import json
import asyncio
from typing import Optional

from app.abus_ffmpeg import *


import structlog
logger = structlog.get_logger()



async def read_stream(stream, progress_callback=None):
    buffer_size = 1024  
    while True:
        output = await stream.read(buffer_size)
        if not output:  # 프로그램 종료 확인
            break
        
        output = output.decode('utf-8', errors='replace').strip()
        if progress_callback:
            progress_callback(output)

async def run_command(command, progress_callback=None):
    try:
        if isinstance(command, list):
            decoded_command = []
            for item in command:
                if isinstance(item, bytes):
                    decoded_command.append(item.decode('utf-8'))  # UTF-8 디코딩
                else:
                    decoded_command.append(item)
            
            # create_subprocess_exec 사용
            process = await asyncio.create_subprocess_exec(
                *decoded_command,  # 리스트 unpacking
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        elif isinstance(command, str): # 문자열 command 처리
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            raise TypeError("command data type error")
    
        # process = await asyncio.create_subprocess_shell(
        #     command,
        #     stdout=asyncio.subprocess.PIPE,
        #     stderr=asyncio.subprocess.PIPE,
        #     creationflags=subprocess.CREATE_NO_WINDOW
        # )

        tasks = [
            # read_stream(process.stdout, progress_callback),
            read_stream(process.stderr, progress_callback)
        ]
        await asyncio.gather(*tasks)

        return_code = await process.wait()
        return return_code
    
    except TypeError as e:
        print(e)
        return None

    
def start_program(command, progress_callback=None):
    return asyncio.run(run_command(command, progress_callback))




def vsr_artifact_reduction(maxine_sdk_path, input_path, output_path, var_mode, progress_callback = None):
    if not os.path.exists(input_path):
        logger.error(f'[abus_vsr.py] vsr_artifact_reduction - Input file not found: {input_path}')
        return False    
        
    maxine_exe_path = os.path.join(maxine_sdk_path, 'VideoEffectsApp.exe')
    maxine_model_path = os.path.join(maxine_sdk_path, 'models')
    if not os.path.exists(maxine_exe_path):
        logger.error(f'[abus_vsr.py] vsr_artifact_reduction - maxine_exe_path not found: {maxine_exe_path}')
        return False    
     
    # command = f'"{maxine_exe_path}" --progress --effect=ArtifactReduction --mode={var_mode}'
    # command += f' --model_dir="{maxine_model_path}"'
    # command += f' --in_file="{input_path}"'
    # command += f' --out_file="{output_path}"'
    # logger.debug(f'[abus_vsr.py] vsr_artifact_reduction - command = {command}')    


    # maxine_model_path_encoded = maxine_model_path.encode('utf-8')  # 파일명 UTF-8로 인코딩
    # maxine_exe_path_encoded = maxine_exe_path.encode('utf-8')  # 파일명 UTF-8로 인코딩
    # input_path_encoded = input_path.encode('utf-8')  # 파일명 UTF-8로 인코딩
    # output_path_encoded = output_path.encode('utf-8')  # 파일명 UTF-8로 인코딩
    
    # command = [
    #     f'{maxine_exe_path_encoded}', 
    #     '--progress',  
    #     '--effect=SuperRes',
    #     f'--mode={var_mode}',
    #     f'--model_dir={maxine_model_path_encoded}',
    #     f'--in_file={input_path_encoded}',
    #     f'--resolution={vsr_resolution}',
    #     f'--out_file={output_path_encoded}'
    # ]   
    
    
    command = [
        f'{maxine_exe_path}', 
        '--progress',  
        '--effect=ArtifactReduction',
        f'--mode={var_mode}',
        f'--model_dir={maxine_model_path}',
        f'--in_file={input_path}',
        f'--out_file={output_path}'
    ]       
    
    logger.debug(f'[abus_vsr.py] vsr_artifact_reduction - command = {command}')    

    try:
        return_code = asyncio.run(run_command(command, progress_callback))
        if return_code != 0:
            logger.error(f"[abus_vsr.py] vsr_artifact_reduction - VideoEffectsApp.exe exited with code {return_code}")
            return False
        return True
    
    except Exception as e:
        logger.error(f"[abus_vsr.py] vsr_artifact_reduction - Error occurred: {e}")
        return False   




def vsr_super_res(maxine_sdk_path, input_path, output_path, vsr_mode, vsr_resolution, progress_callback = None):
    if not os.path.exists(input_path):
        logger.error(f'[abus_vsr.py] vsr_super_res - Input file not found: {input_path}')
        return False    
        
    maxine_exe_path = os.path.join(maxine_sdk_path, 'VideoEffectsApp.exe')
    maxine_model_path = os.path.join(maxine_sdk_path, 'models')
    if not os.path.exists(maxine_exe_path):
        logger.error(f'[abus_vsr.py] vsr_super_res - maxine_exe_path not found: {maxine_exe_path}')
        return False    
     
    # command = f'"{maxine_exe_path}" --progress --effect=SuperRes --mode={vsr_mode}'
    # command += f' --model_dir="{maxine_model_path}"'
    # command += f' --in_file="{input_path}"'
    # command += f' --resolution={int(vsr_resolution)}'
    # command += f' --out_file="{output_path}"'
    # logger.debug(f'[abus_vsr.py] vsr_super_res - command = {command}')    
     

    # maxine_model_path_encoded = maxine_model_path.encode('utf-8')  # 파일명 UTF-8로 인코딩
    # maxine_exe_path_encoded = maxine_exe_path.encode('utf-8')  # 파일명 UTF-8로 인코딩
    # input_path_encoded = input_path.encode('utf-8')  # 파일명 UTF-8로 인코딩
    # output_path_encoded = output_path.encode('utf-8')  # 파일명 UTF-8로 인코딩
    
    # command = [
    #     f'{maxine_exe_path_encoded}', 
    #     '--progress',  
    #     '--effect=SuperRes',
    #     f'--mode={vsr_mode}',
    #     f'--model_dir={maxine_model_path_encoded}',
    #     f'--in_file={input_path_encoded}',
    #     f'--resolution={vsr_resolution}',
    #     f'--out_file={output_path_encoded}'
    # ]   
    
    command = [
        f'{maxine_exe_path}', 
        '--progress',  
        '--effect=SuperRes',
        f'--mode={vsr_mode}',
        f'--model_dir={maxine_model_path}',
        f'--in_file={input_path}',
        f'--resolution={int(vsr_resolution)}',
        f'--out_file={output_path}'
    ]       
    
    logger.debug(f'[abus_vsr.py] vsr_super_res - command = {command}')    

    try:
        return_code = asyncio.run(run_command(command, progress_callback))
        if return_code != 0:
            logger.error(f"[abus_vsr.py] vsr_super_res - VideoEffectsApp.exe exited with code {return_code}")
            return False
        return True
    
    except Exception as e:
        logger.error(f"[abus_vsr.py] vsr_super_res - Error occurred: {e}")
        return False   

   

def vsr_compress_video(
    input_path: str, 
    output_path: str, 
    target_size_mb: Optional[int] = None,
    crf: int = 23,
    preset: str = 'medium',
    progress_callback = None
) -> bool:
    """
    비디오 파일을 압축합니다.
    
    Args:
        input_path (str): 입력 비디오 파일 경로
        output_path (str, optional): 출력 비디오 파일 경로. 
                                    지정하지 않으면 입력 파일 이름에 '_compressed' 추가
        target_size_mb (int, optional): 원하는 최대 파일 크기 (MB)
        crf (int): 압축 품질 조절 (0-51, 낮을수록 고품질. 디폴트 23)
        preset (str): 압축 속도와 효율성 조절 (ultrafast, superfast, veryfast, faster, fast, medium, slow, slower, veryslow)
    
    Returns:
        bool: 압축 성공 여부
    """
    if not os.path.exists(input_path):
        logger.error(f'[abus_vsr.py] vsr_compress_video - Input file not found: {input_path}')
        return False
    
    # input_path_encoded = input_path.encode('utf-8')  # 파일명 UTF-8로 인코딩
    # output_path_encoded = output_path.encode('utf-8')  # 파일명 UTF-8로 인코딩

    # 기본 FFmpeg 압축 명령어
    command = [
        'ffmpeg', 
        '-y',  # 기존 파일 덮어쓰기
        '-i', input_path,
        '-vcodec', 'libx264',  # H.264 비디오 코덱
        '-acodec', 'aac',  # AAC 오디오 코덱
        '-crf', str(crf),  # 압축 품질 (0-51)
        '-preset', preset,  # 압축 속도/효율성
        '-pix_fmt', 'yuv420p',  # 호환성을 위한 픽셀 포맷
    ]

    try:
        # 목표 파일 크기가 지정된 경우
        if target_size_mb:
            # 현재 파일 크기 확인
            original_size = os.path.getsize(input_path) / (1024 * 1024)  # MB 단위
            
            # 목표 크기에 따라 CRF 값 동적 조정
            if original_size > target_size_mb:
                # 대략적인 CRF 조정 로직 (실제 결과는 다를 수 있음)
                adjust_factor = original_size / target_size_mb
                new_crf = min(max(int(crf * adjust_factor), 0), 51)
                command[command.index('-crf') + 1] = str(new_crf)
                logger.info(f"Adjusted CRF to {new_crf} for target size {target_size_mb}MB")
        
        # 최종 출력 경로 추가
        command.append(output_path)
        logger.debug(f'[abus_vsr.py] vsr_compress_video - command = {command}')        
        
        # FFmpeg 실행
        asyncio.run(run_command(command, progress_callback))
        return True
    
    except Exception as e:
        logger.error(f"[abus_vsr.py] vsr_compress_video - Error occurred: {e}")
        return False   