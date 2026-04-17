# Matrix Assessment Report

> [!TIP]
> Use this document to record your progress, the problems you faced and how you solved (or avoided) them.
> You can include images or add files in this directory if you want.

### Summary 

- **implementation**: Synapse  
- **server**: Wheatley - k8s cluster by csesoc   
- **storage**: k8s pvc for SQLite   

### Manifests 

- `pvc.yaml` - request persistent storage from cluster so that messages, accounts, signing keys are not wiped every time the pod restarts.  
- `config.yaml` - configmap stores config data/two key files that get mounted into the container 
    - `homeserver.yaml` - Synapse's main config 
    - `log.config` - Python logging config
- `deployment.yaml` - 


### Procedure 

1. login to wheatley 
2. create k8s namespace `elaine-matrix`
3. create ConfigMap -> apply 

    `log.config` - defines how logs are handled -> debugging

    `homeserver.yaml`

    ```
    server_name: "elaine-matrix.platso.cc"
    ```

    - defines identity in the Matrix network - is domain suffix for all user ids created on this homeserver 
    - value cannot be changed once server started 
    - baked into signing key & federation history and is how other Matrix servers communicate with yours during federation

    ```
    public_baseurl: "https://elaine-matrix.platso.cc"
    ```

    - public facing url clients to reach the homeserver   

    ```
    signing_key_path: /data/elaine-matrix.platso.cc.signing.key
    ```

    - where Synapse stores cryptographic signing key (lives on pvc) - other homeservers use this key to verify federation traffic is legit 

    ```
    listeners:
        - port: 8008
            tls: false           
            x_forwarded: true   
            resources:
                - names: [client, federation] 
    ```

    - listen on port 8008
    - TLS is handled by Cloudflare 
    - let server know its running behind a reverse proxy -> trust the client IP passed through the proxy
    - serve both APIs (client, fed) on the same port
    
4. create pvc -> apply

## Matrix Handle

`@elaine:elaine-matrix.platso.cc`
