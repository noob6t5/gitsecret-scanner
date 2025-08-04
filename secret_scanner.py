import os,sys,subprocess


def run_scanners(repo_path,output_path):
      os.makedirs(output_path,exist_ok=True)
      repo_name=os.path.basename(repo_path)

      truffle_out= os.path.join(output_path,f"{repo_name}_trufflehog.json")
# Avoiding Git leak as it gave more false postive
      print(f"Scanning {repo_name}....")

      try:
            subprocess.run(["trufflehog","filesystem",repo_path,"--json","--no-update"],
                           stdout=open(truffle_out,"w"),stderr=subprocess.DEVNULL)
# Will add with more command's and custom regex
            print(f"{repo_name}")
      except Exception as e:
            print(f"Error scanning {repo_name}: {e}")       


def main(org):
      base_dir =f"repos_{org}"
      output_dir=f"output/{org}/secrets"
      



if  __name__ == "__main__":
    if len(sys.argv)<2:
           print("Usage: python3 secret_scanner.py <directory>")
           sys.exit(1)
    main(sys.argv[1].strip)