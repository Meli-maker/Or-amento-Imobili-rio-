# RentSmart — Sistema de Orçamento de Locação

Projeto acadêmico em Python para automatizar os orçamentos de locação da R.M Imóveis.

## Requisitos
- Python 3.8 ou superior.
- Nenhuma biblioteca externa é necessária.

## Como executar
1. Extraia o ZIP.
2. Abra a pasta `RentSmart` no Visual Studio Code.
3. Abra **Terminal > Novo Terminal**.
4. Digite `python rentsmart.py`. No Windows, se necessário, use `py rentsmart.py`.
5. Responda às perguntas exibidas.
6. O arquivo `projecao_rentsmart.csv` será criado na mesma pasta.

## Regras implementadas
- Apartamento: R$ 700,00; para dois quartos, adicional de R$ 200,00.
- Casa: R$ 900,00; para dois quartos, adicional de R$ 250,00.
- Estúdio: R$ 1.200,00.
- Casa/apartamento: uma vaga por R$ 300,00.
- Estúdio: até duas vagas por R$ 250,00; cada vaga acima de duas custa R$ 60,00.
- Apartamento sem crianças: desconto de 5% após os adicionais.
- Taxa contratual: R$ 2.000,00, dividida em 1 a 5 parcelas.

## Classes
- `Imovel`: classe abstrata com atributos e métodos comuns.
- `Apartamento`, `Casa` e `Estudio`: classes especializadas que implementam suas regras.
- `Orcamento`: calcula os valores e monta a projeção.
- `salvar_csv`: grava os 12 meses em CSV.

## Premissa adotada
O enunciado não define o preço de mais de uma vaga para casas e apartamentos. Para não inventar uma tarifa, o programa permite 0 ou 1 vaga nesses imóveis. Para estúdios, aceita 0 ou mais vagas conforme a regra fornecida.

## Teste sugerido
Apartamento de 2 quartos, uma vaga, sem crianças e taxa em 5 parcelas:
- Subtotal: R$ 700 + R$ 200 + R$ 300 = R$ 1.200.
- Desconto de 5%: R$ 60.
- Aluguel mensal: R$ 1.140.
- Taxa contratual: 5 parcelas de R$ 400.
- Meses 1 a 5: total previsto de R$ 1.540 por mês.
- Meses 6 a 12: total previsto de R$ 1.140 por mês.
