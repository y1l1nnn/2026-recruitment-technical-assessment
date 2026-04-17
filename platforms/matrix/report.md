# Matrix Assessment Report

> [!TIP]
> Use this document to record your progress, the problems you faced and how you solved (or avoided) them.
> You can include images or add files in this directory if you want.

> [in progress...]

### Summary 

- **implementation**: Synapse  
- **server**: Wheatley - k8s cluster by csesoc   
- **storage**: k8s pvc for SQLite   

### Manifests 

- `pvc.yaml` - request persistent storage from cluster so that messages, accounts, signing keys are not wiped every time the pod restarts.  
- `config.yaml` - configmap stores config data/two key files that get mounted into the container 
    - `homeserver.yaml` - Synapse's main config 
    - `log.config` - Python logging config
- `deployment.yaml` - defines Synapse pod (what container, num replicas, config)
- `httproute.yaml` - migrated from istio gateway to gateway api (reverse proxy to route traffic) 
- `service.yaml` - expose Synapse internally within cluster on port 8008 (anything within cluster can reach w)

### Procedure 

1. login to wheatley 
2. create k8s namespace `elaine-matrix`
3. create a DNS record
    - A | elaine-matrix | Wheatley IP | Proxied
5. create pvc -> apply (create storage)
6. create configmap -> apply (apply config)

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
  
    ```
    enable_registration: true
    enable_registration_without_verification: true
    ```

    - allows new user creation + shared secret allows admin
  
    ```
    serve_server_wellknown: true
    ```

    - makes Synapse automatically serve
        - `/.well-known/matrix/server` -> `{"m.server":"elaine-matrix.platso.cc:443"}`
        - `/.well-known/matrix/client` -> `{"m.homeserver":{"base_url":"https://elaine-matrix.platso.cc"}}`
      for federation and tells other servers to connect to port 443 instead rather than default 8448
    
7. create deployment -> apply (deploy synapse)
8. create service -> apply (expose internally) 
9. create httproute -> apply (expose externally)
10. verify synapse is reachable

   ```
   curl https://elaine-matrix.platso.cc/_matrix/client/versions
   # Returns JSON list of supported Matrix versions

   curl https://elaine-matrix.platso.cc/.well-known/matrix/server
   # Returns {"m.server":"elaine-matrix.platso.cc:443"}
   ```
11. create user -> login -> send msg

## Matrix Handle

`@elaine:elaine-matrix.platso.cc`
