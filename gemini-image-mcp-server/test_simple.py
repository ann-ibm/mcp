import json
import sys
import os

def send_simple_command():
    # 构造一个简单的 MCP 命令
    command = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "generate_image",
        "params": {
            "prompt": "a river with a dam that has some broken sections on one side, showing water flowing through the damaged area"
        }
    }
    
    # 发送命令
    print(json.dumps(command))
    sys.stdout.flush()
    
    # 读取响应
    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            print("Received:", line.strip(), file=sys.stderr)
        except Exception as e:
            print(f"Error reading response: {e}", file=sys.stderr)
            break

if __name__ == "__main__":
    # 设置环境变量
    
    print("Starting test...", file=sys.stderr)
    send_simple_command() 
