
# import os
# import subprocess
# import json
# import glob

# def test_pdf(pdf_name):
#     print(f"\nTesting {pdf_name}...")
#     # Clear previous outputs
#     for f in glob.glob("output/*.json"):
#         os.remove(f)
    
#     # Run processor
#     try:
#         subprocess.run([
#             "docker", "run", "--rm",
#             "-v", f"{os.getcwd()}/input:/app/input",
#             "-v", f"{os.getcwd()}/output:/app/output",
#             "pdf-processor"
#         ], check=True, capture_output=True, text=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Processor failed: {e.stderr}")
#         return False

#     # Verify output
#     json_name = pdf_name.replace('.pdf', '.json')
#     json_path = os.path.join("output", json_name)
    
#     if not os.path.exists(json_path):
#         print(f"❌ Output not generated: {json_path}")
#         print("Existing outputs:", os.listdir("output"))
#         return False
        
#     with open(json_path, 'r', encoding='utf-8') as f:
#         data = json.load(f)
#         print(f"Title: {data['title']}")
#         print(f"Headings: {len(data['outline'])} found")
#         print(f"Language: {data['metadata'].get('detected_language', 'en')}")
    
#     print("✓ Test passed\n")
#     return True

# if __name__ == "__main__":
#     test_cases = [
#         "simple.pdf",
#         "complex.pdf",  # Now handled properly
#         "japanese.pdf"
#     ]
    
#     passed = 0
#     for case in test_cases:
#         if test_pdf(case):
#             passed += 1
    
#     print(f"{passed}/{len(test_cases)} tests passed")
#     sys.exit(0 if passed == len(test_cases) else 1)

import os
import subprocess
import json
import glob
import sys

def test_pdf(pdf_name):
    print(f"\nTesting {pdf_name}...")
    
    # Clear previous outputs
    for json_file in glob.glob("output/*.json"):
       try:
           os.remove(json_file)
       except FileNotFoundError:
          pass
    
    # Run processor
    try:
        result = subprocess.run(
            ["docker", "run", "--rm",
             "-v", f"{os.getcwd()}/input:/app/input",
             "-v", f"{os.getcwd()}/output:/app/output",
             "pdf-processor"],
            capture_output=True,
            text=True,
            check=True
        )
        # Print processor output
        print("Processor output:")
        print(result.stdout)
        if result.stderr:
           print("Errors:", result.stderr)
    except subprocess.CalledProcessError as e:
       print(f"❌ Processor failed with code {e.returncode}")
       print("Output:", e.stdout)
       print("Errors:", e.stderr)
       return False

    # Verify output
    json_name = pdf_name.replace('.pdf', '.json')
    json_path = os.path.join("output", json_name)
    
    if not os.path.exists(json_path):
       print(f"❌ Output not generated: {json_path}")
       print("Existing outputs:", os.listdir("output"))
       return False
        
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Title: {data['title']}")
        print(f"Headings: {len(data['outline'])} found")
        print(f"Language: {data['metadata'].get('detected_language', 'en')}")
    except Exception as e:
       print(f"❌ JSON read error: {str(e)}")
       return False
    
    print("✓ Test passed\n")
    return True

if __name__ == "__main__":
    test_cases = [
        "simple.pdf",
        "complex.pdf",
        "japanese.pdf"
    ]
    
    passed = 0
    for case in test_cases:
        if test_pdf(case):
            passed += 1
    
    print(f"Summary: {passed}/{len(test_cases)} tests passed")
    sys.exit(0 if passed == len(test_cases) else 1)