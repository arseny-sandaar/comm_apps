# Living Stokc Analytics

This project consists of three python apps which communicate between each other:
1. `input.py` enables to set number of animals in a living stock and the regularity (in seconds) of the messages sent by the second tool
2. `generator.py` forms a message of tuples (x, y) in WSG84 for those animals (id) which send their location, i.e., each time the messages consist of coordinates of different set of animals mimicing asynchronousity of a tracking device.
3. `analytics.py` reports received message and calculates the last traveled distances for the animals whose coordinates were sent. Moreover, it calculates the total distance traveled by each animal.

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
