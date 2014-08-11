from pygithub3 import Github
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import re

# display a network graph of followers on github based on a central github user

def auth(login='12Siva', password='****'):
    # Authentication for github
    gh = Github(login=login, password=password)
    main_user = gh.users.get() # Auth required
    return gh

def repo_language(user):
    # get the most common language of the user by looking at repo and finding each programming language
    repositories = gh.repos.list(user=user).all() # all the users repositories
    language_list = []
    for repo in repositories:
        try:
            language = repo.language
            language_list.append(language)
        except:
            print "Repository Error"

    languageCounter = Counter(language_list)
    if len(languageCounter.most_common(1)) != 0:
        return languageCounter.most_common(1)[0][0]
    else:
        return None


def followers(user=None):
    # generator to return the usernames of every follower
    user_followers = gh.users.followers.list(user=user).all()
    for follower in user_followers:
        # parse the username from the format returned by the api
        match = re.search('User\s\(((\w+-*)+)\)', str(follower))
        if (match != None) and (match.group(1) != 'hcilab'):
            #print "UserName: " + str(match.group(1))
            yield match.group(1)
        else:
            print follower
            print "**Parsing Error**"

def mututal_followers(user):
    # print out if you are following one of the followers of the user
    followers_gen = followers(user=user)
    for follower in followers_gen:
     # check to see if the the follower is being followed by you
     if gh.users.followers.is_following(user=follower):
         print "***Mutual Followers: " + str(follower)
     else:
         print follower + " follows " + test_user

def followers_graph(nodes, edges):
    # display a network graph of followers
    # directed graph, points to the user being followed
    # Assumption: a user will not follow themselves so there are no loops
    G = nx.DiGraph() # directed graph
    pos = nx.spring_layout(G)

    G.add_nodes_from(nodes) # nodes
    G.add_edges_from(edges) # edges

    # node_size = []
    # for node in G.nodes():
    #     # size of each node is slightly depend on the number of followers of the user
    #     size = 550 * followers_dict[node]
    #     # place lower and upper bounds on the size of each node for visual appeal
    #     if size > 20000:
    #      node_size.append(20000)
    #     elif size < 1000:
    #      node_size.append(1000)
    #     else:
    #      node_size.append(size)

    nx.draw_networkx(G, node_size=20000, with_labels=True, node_color='#3333FF', alpha=0.8)
    #l = nx.draw_networkx_labels(G, pos=nx.spring_layout(G), labels=labels, font_size=17)

    # matplotlib options for the final plot
    plt.axis('off')
    plt.savefig('GitHub-Follower-Network.png')
    plt.show()

def num_followers(user):
    # helper function for sorting based on number of followers
    return followers_dict[user]

def most_followed(user):
    # return the 10 followers of user who are the most followed
    followers_gen = followers(user)
    # dict to correlate username to number of followers
    for follower in followers_gen:
        num = len(gh.users.followers.list(user=follower).all())
        followers_dict[follower] = num

    # sort the dict into decreasing order and place into a list based on the number of followers of the user
    followers_list = sorted(followers_dict, key=num_followers, reverse=True)
    return followers_list[:4]

def edges(main_user):
    # determine all the edges (follower relationships) in the network
    main_userLabel = str(main_user) + '(' + str(repo_language(main_user)) + ')'
    for user in most_followed(main_user):
        userLabel = str(user) + '(' + str(repo_language(user)) + ')'
        edge_tuple = (userLabel, main_userLabel)
        followers_nodes.append(userLabel)
        followers_edges.append(edge_tuple)

def network(test_user):
    initial_nodes = most_followed(user=test_user) # list of only the 10 most followed usernames that follow the user
    followers_dict[test_user] = len(gh.users.followers.list(user=test_user).all()) # add in the root user
    test_userLabel = str(test_user) + '(' + str(repo_language(test_user)) + ')'

    for follower in initial_nodes:
        followerLabel = str(follower) + '(' + str(repo_language(follower)) + ')'
        edge_tuple = (followerLabel, test_userLabel)
        followers_edges.append(edge_tuple)
        edges(follower)

    followers_nodes.append(test_userLabel)
    print followers_nodes
    print followers_edges
    print followers_dict


    followers_graph(followers_nodes, followers_edges)

if __name__ == '__main__':
    gh = auth()
    test_user = '****' # test case user (center of the graph)

    followers_nodes = [] # list of usernames that will represent the vertices of the graph
    followers_edges = [] # list of tuples that will represent the edges of the graph
    followers_dict = {}
    followersLabel_dict = {}

    network(test_user=test_user)