from tcp_data import export_and_process_tcp_data
from excel_file import create_excel_file

def main():
    pcap_files = ['unr.pcapng', 'youtube.pcapng', 'reddit.pcapng', 'amazon.pcapng', 'twitch.pcapng']
    csv_files = ['unr.csv', 'youtube.csv', 'reddit.csv', 'amazon.csv', 'twitch.csv']
    excel_files = ['unr.xlsx', 'youtube.xlsx', 'reddit.xlsx', 'amazon.xlsx', 'twitch.xlsx']

    # Process pcap files and convert them to csv
    for pcap, csv in zip(pcap_files, csv_files):
        export_and_process_tcp_data(pcap, csv)

    # Process csv files and convert them to excel with statistics and analysis
    for csv in csv_files:
        create_excel_file(csv)

if __name__ == "__main__":
    main()