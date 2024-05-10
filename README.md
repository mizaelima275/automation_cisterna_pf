# Medidor de Nível de Água para Cisterna

Este é um projeto para medir o nível de água em uma cisterna utilizando um sensor de distância ultrassônico e enviar os dados para o Home Assistant.

## Pré-requisitos

- Microcontrolador ESP32 ou similar
- Sensor de distância ultrassônico HC-SR04
- Acesso à rede Wi-Fi
- Conta no Home Assistant com token de acesso para API

## Instalação e Configuração

1. Conecte o sensor de distância ultrassônico ao microcontrolador de acordo com o esquemático fornecido no código.
2. Modifique as seguintes variáveis no código de acordo com a sua configuração:
   - `ssid`: Nome da sua rede Wi-Fi.
   - `password`: Senha da sua rede Wi-Fi.
   - `url`: URL da API do Home Assistant para enviar os dados.
   - `token`: Token de acesso para a API do Home Assistant.
   - `altura_maxima`: Altura máxima da cisterna em cm.
   - `altura_minima`: Altura mínima da cisterna em cm.
3. Carregue o código para o seu microcontrolador.

## Uso

Ao ser inicializado, o dispositivo irá conectar-se à rede Wi-Fi e começar a medir o nível de água na cisterna. Os dados são enviados para o Home Assistant periodicamente. Certifique-se de que o sensor está devidamente posicionado para medir o nível de água corretamente.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir uma issue ou enviar um pull request.
