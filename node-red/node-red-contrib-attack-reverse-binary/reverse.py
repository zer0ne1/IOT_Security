from capstone import *
import sys
import json


arch_map = {
    "CS_ARCH_X86": CS_ARCH_X86,
    "CS_ARCH_ARM": CS_ARCH_ARM,
    "CS_ARCH_ARM64": CS_ARCH_ARM64,
    "CS_ARCH_MIPS": CS_ARCH_MIPS,
    "CS_ARCH_PPC": CS_ARCH_PPC,
    "CS_ARCH_SPARC": CS_ARCH_SPARC,
    "CS_ARCH_SYSZ": CS_ARCH_SYSZ,
    "CS_ARCH_XCORE": CS_ARCH_XCORE
}

mode_map = {
    "CS_MODE_LITTLE_ENDIAN": CS_MODE_LITTLE_ENDIAN,
    "CS_MODE_ARM": CS_MODE_ARM,
    "CS_MODE_16": CS_MODE_16,
    "CS_MODE_32": CS_MODE_32,
    "CS_MODE_64": CS_MODE_64,
    "CS_MODE_THUMB": CS_MODE_THUMB,
    "CS_MODE_MCLASS": CS_MODE_MCLASS,
    "CS_MODE_V8": CS_MODE_V8,
    "CS_MODE_MICRO": CS_MODE_MICRO,
    "CS_MODE_MIPS3": CS_MODE_MIPS3,
    "CS_MODE_MIPS32R6": CS_MODE_MIPS32R6,
    "CS_MODE_MIPS2": CS_MODE_MIPS2,
    "CS_MODE_V9": CS_MODE_V9,
    "CS_MODE_QPX": CS_MODE_QPX,
    "CS_MODE_M68K_000": CS_MODE_M68K_000,
    "CS_MODE_BIG_ENDIAN": CS_MODE_BIG_ENDIAN
}

def process_json_input(json_string):
    try:
        # Phân tích chuỗi JSON thành một đối tượng Python
        data = json.loads(json_string)
        # Trả về đối tượng đã được phân tích
        return data
    except json.JSONDecodeError as e:
        # Xử lý trường hợp nếu chuỗi JSON không hợp lệ
        print("Invalid JSON format:", e)
        sys.stdout.flush()
        return None
    
def reverse(data,output_file):
    try:
        architectures = arch_map.get(data['architectures'])
        mode = mode_map.get(data['mode'])
        hex_data = ''.join(filter(str.isalnum, data['content']))
        # Chuyển đổi hex thành chuỗi byte
        byte_data = bytes.fromhex(hex_data)
        md = Cs(architectures, mode)
        # Tiến hành dịch ngược
        disassembled_code = ""
        # Tiến hành dịch ngược và lưu trữ kết quả vào chuỗi
        for i in md.disasm(byte_data, 0x1000):  # 0x1000 là địa chỉ bắt đầu (tùy chỉnh nếu cần)
            result = f"0x{i.address:x}:\t{i.mnemonic}\t{i.op_str}\n"
            disassembled_code += result
        # In ra toàn bộ kết quả
        print(disassembled_code)
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(disassembled_code)
    except Exception:
        print("[-] Error reverse")


if __name__ == "__main__":
    data1 = sys.stdin.readline()
    data=process_json_input(data1)
    print("Loading Reverse Binary To Assembly ....................")
    sys.stdout.flush()
    output_file = "output.asm"  # Tên file bạn muốn lưu kết quả
    reverse(data, output_file)
    print(f"Resule saved in {output_file}")
    
