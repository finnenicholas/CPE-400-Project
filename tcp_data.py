import pyshark
import pandas as pd

def export_and_process_tcp_data(pcap_file, csv_file):
    cap = pyshark.FileCapture(pcap_file, display_filter='tcp')

    tcp_data = []
    for packet in cap:
        if 'TCP' in packet:
            packet_info = {
                'Timestamp': packet.sniff_timestamp,
                'Source IP': packet.ip.src,
                'Destination IP': packet.ip.dst,
                'Source Port': packet.tcp.srcport,
                'Destination Port': packet.tcp.dstport,
                'Length': int(packet.length),
                'TCP Flags': packet.tcp.flags,
                'Seq Number': packet.tcp.seq,
                'Ack Number': packet.tcp.ack,
                'Window Size': packet.tcp.window_size_value,
                'TCP Length': packet.tcp.len if hasattr(packet.tcp, 'len') else None,
                'TCP Checksum': packet.tcp.checksum,
            }
            tcp_data.append(packet_info)

    cap.close()

    # Convert to DataFrame
    df = pd.DataFrame(tcp_data)

    # Sorting by Timestamp
    df['Timestamp'] = pd.to_datetime(df['Timestamp'].astype(float), unit='s')

    df.sort_values(by='Timestamp', inplace=True)

    # Grouping and aggregating data
    aggregated_df = df.groupby(['Source IP', 'Destination IP'], as_index=False).agg(
        First_Timestamp=pd.NamedAgg(column='Timestamp', aggfunc='first'),
        Total_Length=pd.NamedAgg(column='Length', aggfunc='sum'),
        Packet_Count=pd.NamedAgg(column='Length', aggfunc='count')
    )

    # Export to CSV
    aggregated_df.to_csv(csv_file, index=False)

    print(f"Processed TCP data exported to {csv_file}")