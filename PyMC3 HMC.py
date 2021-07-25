import pymc3 as pm
import numpy as np
import matplotlib.pyplot as plt
import arviz as az
import theano
import theano.tensor as tt
from MakeTrainingData import make_training_data

from pymc3.math import invlogit, prod
from theano.tensor import pow


def main():
    ### Raw training data ###
    follower_training_data, pol_actor_training_data = make_training_data()

    ### Data for model ###
    J = len(follower_training_data)  # Num of followers
    K = len(pol_actor_training_data)  # Num of actors
    y = [[0 for i in range(K)] for j in range(J)]  # List of observations (does i follow j?)
    N = J * K  # Total obs
    jj = [j for i in range(K) for j in range(1, J + 1)]  # Twitter user for observation n
    kk = [i for i in range(1, K + 1) for j in range(J)]  # Pol. actor for observation n

    pol_actor_map = {}  # Allows us to map political actors to indexes in phi
    i = 0
    for actor, data in pol_actor_training_data.items():
        pol_actor_map[actor] = i
        i += 1

    i = 0
    for user, data in follower_training_data.items():
        follows = data['follows']
        for actor in follows:  # Check if user follows a political actor
            actor_num = pol_actor_map[actor]
            y[i][actor_num] = 1
        i += 1

    ### Meta data ###
    num_actors = len(pol_actor_training_data)
    num_followers = len(follower_training_data)

    ### Create Model ###
    model = pm.Model()
    with model:

        ### Hyper Priors ###
        mu_beta = pm.Flat(name='mu_beta', testval=0)
        mu_phi = pm.Flat(name='mu_phi', testval=0)
        sigma_beta = pm.Flat(name='sigma_beta', testval=1)
        sigma_phi = pm.Flat(name='sigma_phi', testval=1)
        sigma_alpha = pm.Flat(name='sigma_alpha', testval=1)
        gamma = pm.Flat(name='gamma', testval=abs(np.random.normal(loc=0, scale=1)))

        ### Priors ###
        # R^(j)
        alpha = pm.Normal(name='alpha', mu=0, sigma=sigma_alpha, shape=num_actors,
                          testval=[np.log(float(data[0])) for data in pol_actor_training_data.values()])
        # R^(i)
        beta = pm.Normal(name='beta', mu=mu_beta, sigma=sigma_beta, shape=num_followers,
                         testval=[data['friends_count'] for user, data in follower_training_data.items()])
        # R^(j)
        phi = pm.Normal(name='phi', mu=mu_phi, sigma=sigma_phi, shape=num_actors,
                        testval=[float(data[1]) for data in pol_actor_training_data.values()])
        # R^(i)
        theta = pm.Normal(name='theta', mu=0, sigma=1, shape=num_followers,
                          testval=np.random.normal(loc=0, scale=1, size=len(follower_training_data)))  # TODO: CHECK LOC & SCALE

        ### Define pi ###
        i = num_followers
        j = num_actors
        alpha_M = pm.math.stack([alpha in range(i)], axis=1)        # R^(j x i)
        beta_M = pm.math.stack([beta in range(j)])                  # R^(j x i)
        phi_M = pm.math.stack([phi in range(i)], axis=1)
        theta_M = pm.math.stack([theta in range(j)])

        ab = alpha_M + beta_M
        tpg = (theta_M - phi_M) * gamma

        pi = ab - tpg   # R^(j x i)

        ### Find the (proportional) likelihood ###
        invlogit_pi = invlogit(pi)
        log_likelihood = prod(pow(invlogit_pi, y)) * prod(pow(1-invlogit_pi, y))

        y_obs = pm.Bernoulli(name='Likelihood', p=log_likelihood, observed=y)


    # Train
    with model:
        trace = pm.sample(2_000, cores=1, init='adapt_diag')
        az.plot_trace(trace)
        plt.show()


if __name__ == '__main__':
    main()