import pystan as stan
import numpy as np
import tensorflow as tf
import tensorflow_probability as tfp

tfd = tfp.distributions


def main():
    # # Training data
    # def make_training_data():
    #     with open('Old files/TwitterData (Larger Version).npz', 'rb') as npzfile:
    #         with open('Old files/PoliticalActorFollowers.npz', 'rb') as actor_data:
    #             saved_follower_data = np.load(file=npzfile, allow_pickle=True)['arr_0'].item()
    #             # pol_actor_followers = np.load(file=actor_data, allow_pickle=True)['arr_0'].item()
    #             pol_actor_followers = {'BarackObama': (126598255, -1), 'realDonaldTrump': (88910434, 1),
    #                                    'HillaryClinton': (29809594, -1), 'POTUS': (32910893, 0),
    #                                    'POTUS44': (14651507, -1),
    #                                    'AOC': (10571737, -1), 'SenSanders': (10864474, -1),
    #                                    'BernieSanders': (13868680, -1),
    #                                    'SenWarren': (6570108, -1), 'BillClinton': (12791855, -1),
    #                                    'KamalaHarris': (12218284, -1), 'ObamaWhiteHouse': (12709675, -1),
    #                                    'FLOTUS': (16109103, 0), 'JoeBiden': (19561930, -1), 'VP': (10188610, 0),
    #                                    'PressSec': (6195526, 0), 'tedlieu': (1498796, -1), 'Emma4Change': (1534815, -1),
    #                                    'SpeakerPelosi': (6020766, -1), 'FLOTUS44': (6457204, -1),
    #                                    'mike_pence': (5890972, 1), 'BetoORourke': (1824457, -1),
    #                                    'SenSchumer': (2788937, -1), 'RepMaxineWaters': (1584427, -1),
    #                                    'ewarren': (5283385, -1), 'RepAdamSchiff': (2697858, -1),
    #                                    'Acosta': (2037693, -1),
    #                                    'CoryBooker': (4771754, -1), 'repjohnlewis': (1242256, -1),
    #                                    'VP44': (2515061, -1),
    #                                    'SenKamalaHarris': (4143717, -1), 'shaunking': (1154000, 0),
    #                                    'davidhogg111': (1043010, -1), 'SpeakerRyan': (3610308, 1),
    #                                    'SenFeinstein': (1497001, -1), 'tedcruz': (4174945, 1),
    #                                    'RyanAFournier': (1131332, 1), 'alfranken': (907796, -1),
    #                                    'amyklobuchar': (1324406, -1), 'AndrewGillum': (621796, -1),
    #                                    'charliekirk11': (1917389, 1), 'SenGillibrand': (1603817, -1),
    #                                    'LindseyGrahamSC': (2016097, 1), 'algore': (3045657, -1),
    #                                    'GovMikeHuckabee': (1770779, 1), 'MittRomney': (2135037, 1),
    #                                    'newtgingrich': (2409805, 1), 'RealBenCarson': (2382150, 1),
    #                                    'SenJohnMcCain': (3008695, 1), 'marcorubio': (4272484, 1),
    #                                    'RandPaul': (3028876, 1),
    #                                    'SarahPalinUSA': (1504442, 1), 'RepCummings': (535970, -1),
    #                                    'RepJoeKennedy': (815726, -1), 'AmbNikkiHaley': (1547904, 1),
    #                                    'IlhanMN': (2643981, -1), 'deray': (1066825, -1), 'JasonKander': (369508, -1),
    #                                    'JohnKerry': (3381688, -1), 'Jim_Jordan': (1915898, 1),
    #                                    'JustinTrudeau': (5310726, -1), 'MELANIATRUMP': (1334372, 1),
    #                                    'SenDuckworth': (719989, -1), 'NikkiHaley': (724079, 1),
    #                                    'timkaine': (999943, -1),
    #                                    'SenFranken': (444339, -1), 'ChrisMurphyCT': (988120, -1),
    #                                    'DanCrenshawTX': (1120987, 1), 'GavinNewsom': (1957695, -1),
    #                                    'norm': (651453, -1),
    #                                    'staceyabrams': (1551998, -1), 'Im_TheAntiTrump': (224740, -1),
    #                                    'Sarahchadwickk': (284980, 0), 'TGowdySC': (1259541, 1),
    #                                    'cameron_kasky': (394242, -1), 'shannonrwatts': (489406, 0),
    #                                    'RepSwalwell': (913239, -1), 'SenTedCruz': (1827603, 1),
    #                                    'SteveWestly': (228995, -1),
    #                                    'SenatorCollins': (568401, 1), 'SenatorDurbin': (681062, -1),
    #                                    'SecPompeo': (2646644, 1), 'senatemajldr': (2090060, 1),
    #                                    'RashidaTlaib': (1242735, -1), 'mmpadellan': (774341, 0),
    #                                    'SenBlumenthal': (689181, -1), 'VicenteFoxQue': (1372596, 0),
    #                                    'AyannaPressley': (856162, -1), 'SpeakerBoehner': (1357290, 1),
    #                                    'DearAuntCrabby': (276760, 0)}
    #
    #             return saved_follower_data, pol_actor_followers

    # follower_training_data, pol_actor_training_data = make_training_data()

    # NOTE: The values of the *training data* (ie. follower_training_data and pol_actor_training_data) are
    # NOT intended to be altered at any point in these nodes. Only the TF variables assigned above are. If
    # the raw training data is altered at any point, these indexes below will fail.

    # Allows us to map political actors to indexes in phi
    pol_actor_map = {}
    i = 0
    for actor, data in pol_actor_training_data.items():
        pol_actor_map[actor] = i
        i += 1

    # Initializations for chain
    beta = [data['friends_count'] for user, data in follower_training_data.items()]
    alpha = [np.log(float(data[0])) for data in pol_actor_training_data.values()]
    theta = tfd.Normal(loc=tf.zeros_like(beta, dtype=np.float32),
                       scale=tf.ones_like(beta, dtype=np.float32)).sample().numpy().tolist()
    phi = [float(data[1]) for data in pol_actor_training_data.values()]
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
    fit = model.sampling(init=inits, data=data, iter=500, warmup=100, chains=2, thin=1, n_jobs=2, sample_file="model_samples")


if __name__ == '__main__':
    main()
