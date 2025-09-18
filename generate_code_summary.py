# generate_code_summary.py
import os

def summarize_directory(root_dir, max_file_size_kb=100):
    summary = []

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_dir)

            # Only read small text files
            if filename.endswith(('.py', '.html', '.txt', '.cfg')) and os.path.getsize(filepath) <= max_file_size_kb * 1024:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                summary.append({
                    'path': rel_path.replace("\\", "/"),
                    'content': content
                })
            else:
                summary.append({
                    'path': rel_path.replace("\\", "/"),
                    'content': '[Skipped: Too large or not a relevant file type]'
                })
    return summary

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    summary = summarize_directory(project_root)

    output_file = os.path.join(project_root, 'project_summary.txt')
    with open(output_file, 'w', encoding='utf-8') as f:
        for file in summary:
            f.write(f"\n{'='*80}\n")
            f.write(f"FILE: {file['path']}\n")
            f.write(f"{'-'*80}\n")
            f.write(file['content'] + '\n')
    print(f"\n✅ Project summary generated: {output_file}")

if __name__ == "__main__":
    main()
