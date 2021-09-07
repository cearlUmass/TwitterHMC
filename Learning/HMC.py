import pystan as stan
import pickle
import csv
import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

tfd = tfp.distributions


if __name__ == '__main__':

    # Initializations for chain
    beta = [data['friends_count'] for user, data in follower_data.items()]
    alpha = [np.log(float(data[0])) for data in actor_data.values()]
    theta = tfd.Normal(loc=tf.zeros_like(beta, dtype=np.float32),
                       scale=tf.ones_like(beta, dtype=np.float32)).sample().numpy().tolist()
    phi = [float(data[1]) for data in actor_data.values()]
    gamma = abs(tfd.Normal(loc=0, scale=1).sample()).numpy()


    def inits():
        return {
            'alpha': alpha,
            'phi': phi,
            'theta': theta,
            'beta': beta,
            'mu_beta': 0,
            'mu_phi': 0,
            'sigma_beta': 1,
            'sigma_phi': 1,
            'sigma_alpha': 1,
            'gamma': gamma
        }


    # Data for model
    J = len(follower_training_data)
    K = len(pol_actor_training_data)
    y = [[0 for i in range(K)] for j in range(J)]
    i = 0
    for user, data in follower_training_data.items():
        follows = data['follows']
        for actor in follows:
            actor_num = pol_actor_map[actor]
            y[i][actor_num] = 1
        i += 1

    data = {
        'J': J,
        'K': K,
        'N': J * K,
        'jj': [j for i in range(K) for j in range(1, J + 1)],
        'kk': [i for i in range(1, K + 1) for j in range(J)],
        'y': [follows for l in y for follows in l]
    }

    model = """
        data {
          int<lower=1> J; // number of twitter users
          int<lower=1> K; // number of elite twitter accounts
          int<lower=1> N; // N = J x K
          int<lower=1,upper=J> jj[N]; // twitter user for observation n
          int<lower=1,upper=K> kk[N]; // elite account for observation n
          int<lower=0,upper=1> y[N]; // dummy if user i follows elite j
        }
        parameters {
          vector[K] alpha;
          vector[K] phi;
          vector[J] theta;
          vector[J] beta;
          real mu_beta;
          real<lower=0.1> sigma_beta;
          real mu_phi;
          real<lower=0.1> sigma_phi;
          real<lower=0.1> sigma_alpha;
          real gamma;
        }
        model {
          alpha ~ normal(0, sigma_alpha);
          beta ~ normal(mu_beta, sigma_beta);
          phi ~ normal(mu_phi, sigma_phi);
          theta ~ normal(0, 1); 
          for (n in 1:N)
            y[n] ~ bernoulli_logit( alpha[kk[n]] + beta[jj[n]] - 
              gamma * square( theta[jj[n]] - phi[kk[n]] ) );
        }
    """

    print("COMPILING MODEL...")
    model = stan.StanModel(model_code=model)
    print("RUNNING MODEL...")
    fit = model.sampling(init=inits, data=data, iter=500, warmup=100, chains=2, thin=1, n_jobs=2,
                         sample_file="model_samples")
