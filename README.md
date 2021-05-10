# FashionShoppingApp

The torch in the requirements.txt are CPU version, so that the packages are small enough to be deployed.

Still, the sbert model is too large (400MB) to load in app memory (512MB limit), so the current approach doesn't work. We would need to deploy the model separately and call inference from the API to avoid loading the model.
