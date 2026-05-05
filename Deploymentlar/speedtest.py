import speedtest

def run_speed_test():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        
        # Замеры
        download_speed = st.download()
        upload_speed = st.upload()
        ping = st.results.ping
        
        print("-" * 30)
        print("Result:")
        print("Download: {:.2f} Mbit/s".format(download_speed / 1000000))
        print("Upload:   {:.2f} Mbit/s".format(upload_speed / 1000000))
        print("Ping:     {} ms".format(ping))
        print("-" * 30)
        
    except Exception as e:
        print("Error: {}".format(e))

if __name__ == "__main__":
    run_speed_test()