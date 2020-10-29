<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/LouisKlimek/Scrap-Gold-Prices">
    <img src="logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Scrap Gold Prices</h3>

  <p align="center">
    Get Prices of different Gold Puritys from Gold.de
    <br />
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
* [Contributing](#contributing)
  * [ToDo](#todo)
* [License](#license)



<!-- ABOUT THE PROJECT -->
## About The Project

This is just a Simple Python Class to get Gold Prices from Gold.de. It currently only supports Euro and Gramms!


<!-- GETTING STARTED -->
## Getting Started

To get a gold price just call the getGoldPrice() Function and with your desired Attributes. See following Code:
```sh
#getGoldPrice(karat, currency, unitOfMeasurement)

getGoldPrice("24k", "EUR", "gramm") #Returns the Price of Pure (999) Gold in Euro as a Float

getGoldPrice("333", "EUR", "gramm") #Returns the Price of 8 Karat (333) Gold in Euro as a Float
```

Note that there is currently only support for Euro and Grams!


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- TODO -->
## ToDo

If you decide that you want to help out, here is a little List of things that need to be done.

1. Add support for other currencies
2. Add support for other units (e.g. ounce, kilogram)



<!-- LICENSE -->
## License

Distributed under the Apache License 2.0. See `LICENSE` for more information.
