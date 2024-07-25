# Living Stokc Analytics
## Desription of apps
This project consists of three python apps which communicate between each other through [WebSockets](https://websockets.readthedocs.io/en/stable/):
1. `input.py` enables to set number of animals in a living stock and the regularity `R` (in seconds) of the messages sent to the tool - generator.py. Number of animals inputed by users is a total number of species in the living stock with tracking device. The assigned regularity stand for the frequency of a hub collected all the data from animals' devices.
2. `generator.py` forms a message of coordinates tuples `(x, y)` in WSG84 for those animals' devices (ids) which send their location, i.e., each `R` time the messages consist of coordinates of different set of animals mimicing asynchronousity of tracking devices. We perform it by randomly choosing animals' ids from the given number of species: it is assumed that an animal does not move if there is no position sent from it. The app generates the next position of an animal based on its previous location and the distance it may travel during `R` period. In the app we assume that the speed `V` of an animal may randomly vary from `0` to `2.5 m/s` and will be the same during period `R` meaning the distance animal travels is equal to `R*V`. The app makes available the message to the next tool which listens to at a certain port.
3. `analytics.py` reports received message and calculates the last traveled distances for each animal whose coordinates were sent. Moreover, it calculates the total distance traveled by each animal every time when the message from `generator.py` received.

## Perspectives
Both `generator.py` and 'analytics.py` may be improved. There are a few ideas how one may proceed with `generator.py`:
1. Animals may move but the device may not send its position: one need to simulate such a behaviour.
2. Introduce some constraints keeping animals in a herd, e.g., animals are within an ellipse. 
3. The speed of all animals should be within a notmal distribution.
4. Introduce a turning angle for all the animals to simulate the direction of herd movement.
In the 'analytics.py`, one may think of sinusoity besides positions and distance reporting. Moreover, animal location prediction based on the previous positions may be studied as well as the location of those animals whose coordinates were not sent.  

## Local Development
### Setup

1. **Clone the repository**:
    ```
    git clone https://github.com/arseny-sandaar/comm_apps.git desired_folder
    cd desired_folder
    ```

2. **Install dependencies**:
    ```
    pip install -r requirements.txt
    ```

3. **Run the application**:
   In three different terminals run in the following order each app:
    ```
    python analytics.py
    ```
    ```
    python generator.py
    ```
    ```
    python input.py
    ```
