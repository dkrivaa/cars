import data
import joblib
import numpy as np
import owners

license = 31555401

# owners.owner_data()
# owners.new_cars_by_year_owner()
# car_price = model1.y_pred()

shnat_yitzur, Km, Owner, price = data.data_license(license)

age = int(2024 - shnat_yitzur)
Km = float(Km)
Owner = int(Owner)
price = float(price)

data_array = [np.array((age, Km, Owner))]
print(data_array)
regressor = joblib.load('mlp_regressor_model.joblib')

used_price = regressor.predict(data_array) * price

print(used_price)


