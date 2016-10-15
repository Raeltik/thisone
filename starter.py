#!/usr/bin/env python3.5

import sys
import argparse
import docker
from pprint  import pprint


parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clean', action='store_true', help="used to clean up old or not needed lanes")
parser.add_argument('-l', '--list', action='store_true', help="list currently running lanes")
parser.add_argument('-s', '--start', type=int, help='Start X number of lanes.')
args = parser.parse_args()


def start_team(num, cli):
    for team in range(num):
        team_num = team + 1

        ipam_pool = docker.utils.create_ipam_pool(
            subnet='10.0.{}.0/29'.format(team_num),
            gateway='10.0.{}.4'.format(team_num))

        ipam_config = docker.utils.create_ipam_config(
            pool_configs=[ipam_pool])

        cli.create_network("network{}".format(team_num), driver="bridge", ipam=ipam_config)

        cl1_net_config = cli.create_networking_config({
            'network{}'.format(team_num): cli.create_endpoint_config(
                ipv4_address='10.0.{}.1'.format(team_num),
                aliases=['client{}.1'.format(team_num)]
        )})

        cl2_net_config = cli.create_networking_config({
                                'network{}'.format(team_num): cli.create_endpoint_config(
                                        ipv4_address='10.0.{}.2'.format(team_num),
                                        aliases=['client{}.2'.format(team_num)]
                                 #       links=['client().1'.format(team_num),'client{}.3'.format(team_num)])
                                )})

        cl3_net_config = cli.create_networking_config({
                                'network{}'.format(team_num): cli.create_endpoint_config(
                                        ipv4_address='10.0.{}.3'.format(team_num),
                                        aliases=['client{}.3'.format(team_num)]
                                  #      links=['client{}.2'.format(team_num)])
                                )})

                             
        client1 = cli.create_container(image='cdmx:client.1',
                        ports=[80, 22],
                        networking_config=cl1_net_config,
                        hostname='client{}.1'.format(team_num),
                        name='client{}.1'.format(team_num),
                        host_config=cli.create_host_config(
                            port_bindings={80:int('6{}8'.format(team_num)),
                                           22:int('5{}2'.format(team_num))})
                        )

        client2 = cli.create_container(image='cdmx:client.2',
                        networking_config=cl2_net_config,
                        hostname='client{}.2'.format(team_num),
                        name='client{}.2'.format(team_num))

        client3 = cli.create_container(image='cdmx:client.3',
                        networking_config=cl3_net_config,
                        hostname='client{}.3'.format(team_num),
                        name='client{}.3'.format(team_num))
                
        cur_clients = (client1, client2, client3)
        for x in cur_clients:
            cli.start(container=x)
        print('Team {} is up!'.format(team_num))
                        
def listing(cli):
        print("Listing running containers and their networking")
        for x in cli.containers():
            print("{} :".format(x['Names'][0]))
            pprint(x['NetworkSettings']['Networks'])

def cleaning(cli):
        print("Time to kill the clients")
        for x in cli.containers():
            if 'client' in x['Names'][0]:
                print('removing {}'.format(x['Names'][0]))
                cli.kill(x)
                cli.remove_container(x)
        for x in cli.networks():
            if 'network' in x['Name']:
                print('removing {}'.format(x['Name']))
                cli.remove_network(x['Id'])
                
def main(args):
        cli = docker.Client(base_url='unix://var/run/docker.sock')
        #print(args)

        if args.start:
            if args.start > 0:
                print("Starting {} lanes".format(args.start))
                start_team(args.start, cli)
        else: print("Not starting anything new")
        if args.list == True:
             listing(cli)
        if args.clean == True:
            cleaning(cli)
        #print("Already Running: \n")
	#for x in cli.containers():
	#	print("{} @ {}\n".format(x['Names'][0],x['NetworkSettings']['Networks']['bridge']['IPAddress']))
		
	

	#print("Starting {} more.\n".format(starting))

	#start_team(starting,cli)




if __name__ == '__main__':
        import time
        start_time = time.time()
        main(args)
        print("--- %s seconds ---" % (time.time() - start_time))

