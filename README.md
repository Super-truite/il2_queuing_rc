# il2_queuing_rc
RPC with rabbitmq to safely call IL2 RC from several programs running in parallel.
Use case: when having several script like a discord bot, a script managing server load, another changing mission parameters, concurrent RC call can happen at the same time. Using rabbitmq, we can queue the different calls and execute only one at a time.

remote_console.py from : https://github.com/bobcrane/IL2_DServer_Daemon
