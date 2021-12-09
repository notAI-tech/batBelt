if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Not Supported yet"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Downloading cloudflared (for tunneling)"
    wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz -O cloudflared-darwin-amd64.tgz 2>/dev/null || curl -L -o cloudflared-darwin-amd64.tgz https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz
    tar -xf cloudflared-darwin-amd64.tgz
    rm cloudflared-darwin-amd64.tgz
    mv cloudflared /usr/local/bin/cloudflared
    if [ ! -f /usr/local/bin/cloudflared ]; then
        echo "Downloading cloudflared failed. Your connection might be unstable, please try again later."
        rm cloudflared-darwin-amd64.tgz
        exit 1
    fi

    echo "Downloading batServe"

    wget https://github.com/notai-tech/batbelt/releases/latest/download/batserve-darwin-amd64.pex -O /usr/local/bin/batserve 2>/dev/null || curl -L -o /usr/local/bin/batserve https://github.com/notai-tech/batbelt/releases/latest/download/batserve-darwin-amd64.pex

    if [ ! -f /usr/local/bin/batserve ]; then
        echo "Downloading batserve failed. Your connection might be unstable, please try again later."
        exit 1
    fi

    chmod +x /usr/local/bin/batserve
    
    echo "Done! Run batserve --help"
    
elif [[ "$OSTYPE" == "cygwin" ]]; then
    echo "Not Supported yet"
elif [[ "$OSTYPE" == "msys" ]]; then
    echo "Not Supported yet"
elif [[ "$OSTYPE" == "win32" ]]; then
    echo "Not Supported yet"
elif [[ "$OSTYPE" == "freebsd"* ]]; then
    echo "Not Supported yet"
else
    echo "Not Supported yet"

fi


