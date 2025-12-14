const fs = require("fs");

const filename = "cs-universities.json";

const rawData = fs.readFileSync(filename);
let cities = JSON.parse(rawData);

const rent = [
  {
    "city": "Munich",
    "average_monthly_rent": {
      "price": 1436,
      "currency": "EUR"
    }
  }
];

rent.forEach(element => {
  const index = cities.findIndex(c => c.city === element.city);
  if (index !== -1) {
    cities[index].average_monthly_rent = element.average_monthly_rent;
  }
});

fs.writeFileSync(filename, JSON.stringify(cities, null, 2), "utf-8");