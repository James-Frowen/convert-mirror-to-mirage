import os
import re
import sys

def find_replace(file_data, search_pattern, replacement):
    return re.sub(search_pattern, replacement, file_data)
def find_replace_array(file_data, a):
    for (search_pattern, replacement) in a:
        file_data = re.sub(search_pattern, replacement, file_data)
    return file_data

def process(file_data):
    file_data = find_replace_array(file_data, [
    (
        r'\[Command(\(.*\))?\]',
        r'[ServerRpc\1]'
    ),
    (
        r'(\[ServerRpc\(.*)requiresAuthority = (true|false)(.*\)\])',
        r'\1requireAuthority = \2\3'
    ),
    (
        r'\[TargetRpc\]',
        r'[ClientRpc(target = RpcTarget.Player)]'
    ),
    (
        r'NetworkConnection(:?ToClient|ToServer){0,1}',
        r'INetworkPlayer'
    ),
    (
        r'channel = Channels.(Reliable|Unreliable)',
        r'channel = Mirage.Channel.\1'
    ),
    (
        r'(\.)?connectionToClient',
        r'\1Owner'
    ),
    (
        r'(\.)?isServer',
        r'\1IsServer'
    ),
    (
        r'(\.)?isClient',
        r'\1IsClient'
    ),
    (
        r'(\.)?hasAuthority',
        r'\1HasAuthority'
    ),
    (
        r'(\.)?isLocalPlayer',
        r'\1IsLocalPlayer'
    ),
    (
        r'includeOwner = false',
        r'excludeOwner = true'
    ),
    (
        r'includeOwner = true',
        r'excludeOwner = false'
    ),
    (
        r': NetworkBehaviour',
        r': NetworkBehaviourWithOverrides',
    ),
    (
        r'( *)((?:public|private)? struct \w+) : NetworkMessage',
        r'\1[NetworkMessage]\n\1\2',
    )
    ])

    file_data = find_replace(file_data, 
        r'using Mirror;',
        '''using Mirage;
using Mirage.Authentication;
using Mirage.Authenticators;
using Mirage.Authenticators.SessionId;
using Mirage.Collections;
using Mirage.Components;
using Mirage.DisplayMetrics;
using Mirage.Events;
using Mirage.Logging;
using Mirage.RemoteCalls;
using Mirage.Serialization;
using Mirage.SocketLayer;
using Mirage.SocketLayer.ConnectionTrackers;
using Mirage.Sockets.Udp;
using Mirage.Visibility;'''
    )
    return file_data


def main(directory):
    file_pattern = '.cs'

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(file_pattern):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    file_data = f.read()
                new_data = process(file_data)
                if new_data != file_data:
                    with open(file_path, 'w') as f:
                        f.write(new_data)

if __name__ == '__main__':
    main(sys.argv[1])
