if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Not Supported yet"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Downloading cloudflared (for tunneling)"
    which wget; wget -q --show-progress https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz -O cloudflared-darwin-amd64.tgz
    if [ ! -f cloudflared-darwin-amd64.tgz ]; then
        which curl; curl --progress-bar -L -o cloudflared-darwin-amd64.tgz https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz
    fi
    
    tar -xf cloudflared-darwin-amd64.tgz
    rm cloudflared-darwin-amd64.tgz
    mv cloudflared /usr/local/bin/cloudflared
    if [ ! -f /usr/local/bin/cloudflared ]; then
        echo "Downloading cloudflared failed. Your connection might be unstable, please try again later."
        rm cloudflared-darwin-amd64.tgz
        exit 1
    fi

    echo "Downloading batServe"

    which wget; wget -q --show-progress https://github.com/notai-tech/batbelt/releases/latest/download/batbelt-darwin-amd64.tar -O batbelt-darwin-amd64.tar
    if [ ! -f batbelt-darwin-amd64.tar ]; then
        which curl; curl --progress-bar -L -o batbelt-darwin-amd64.tar https://github.com/notai-tech/batbelt/releases/latest/download/batbelt-darwin-amd64.tar
    fi

    tar -xf batbelt-darwin-amd64.tar
    mv batbelt-darwin-amd64/* /usr/local/bin/
    rm -rf batbelt-darwin-amd64 batbelt-darwin-amd64.tar

    if [ ! -f /usr/local/bin/batbelt ]; then
        echo "Downloading batbelt failed. Your connection might be unstable, please try again later."
        exit 1
    fi

    chmod +x /usr/local/bin/batbelt
    
    echo "Start batserve by running 'batbelt serve'"
    
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


