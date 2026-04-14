```bash
sudo apt install bind9
```



```conf
options {
        directory "/var/cache/bind";

        forwarders {
	    192.168.1.10;
            8.8.8.8;
            1.1.1.1;
        };


        dnssec-validation no;
        
        #listen-on { any; };
        # listen-on-v6 { any; };

        listen-on port 53 { 127.0.0.1; };
        listen-on-v6 { none; };
        forward only;
        allow-query { any; };
    	recursion yes;
    	allow-recursion { any; };
};


```