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


