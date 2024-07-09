import React, { useState, useEffect } from 'react';
import { Chart } from 'react-google-charts';
import EmpresaCard from '../components/EmpresaCard';
import Navbar from '../components/Navbar';
import "./ofertaDoDia.css";
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

function OfertaDoDia() {
  const [dataProducts, setDataProducts] = useState([]);
  const [selectedBar, setSelectedBar] = useState(null);
  const [loadingCard, setLoadingCard] = useState(false);
  const [dataEnterprises, setDataEnterprises] = useState([]);
  const [dataPromotions, setDataPromotions] = useState([{ melhoresPorcentagem: [], melhoresValorBruto: [] }]);
  const [dataProductsTypePromotion, setDataProductsTypePromotion] = useState([{ melhoresPorcentagem: [], melhoresValorBruto: [] }]);
  const [modoOrdenacao, setModoOrdenacao] = useState('Porcentagem');
  const [categories, setCategories] = useState([]);
  useEffect(() => {
  }, [dataPromotions]);

  useEffect(() => {
    fetch('http://localhost:5000/api/products/promotion/cupom')
      .then(response => response.json())
      .then(data => {
        console.log("complete_data")
        console.log(data)
        setCategories(getCategories(data));

        console.log(categories)
      });
  }, []);

  const getCategories = (data) => {
    const categories = data.map(item => item.category);
    return categories

  }
  const getProductsTypeWithMorePromotions = (data) => {
    const indexedData = data.map((item, index) => ({ ...item, originalIndex: index }));

    const productsType = indexedData
      .filter(item => item.type)
      .map(item => item.type);

    const productsTypeWithCount = productsType.reduce((acc, item) => {
      if (!acc[item]) acc[item] = 0;
      acc[item]++;
      return acc;
    }, {});

    const productsTypeWithCountArray = Object.entries(productsTypeWithCount)
      .sort((a, b) => b[1] - a[1]);

    return productsTypeWithCountArray;
  }
  const getBest3Promotions = (data) => {
    const indexedData = data.map((item, index) => ({ ...item, originalIndex: index }));

    const sortedByPorcentagem = indexedData
      .filter(item => item.promotion && item.promotion.porcentagem)
      .sort((a, b) => {
        const porcentagemA = parseFloat(a.promotion.porcentagem.replace('% OFF', ''));
        const porcentagemB = parseFloat(b.promotion.porcentagem.replace('% OFF', ''));
        return porcentagemB - porcentagemA;
      })
      .slice(0, 3);

    const sortedByValorBruto = indexedData
      .filter(item => item.promotion && item.promotion.valorBruto)
      .sort((a, b) => parseFloat(a.promotion.valorBruto) - parseFloat(b.promotion.valorBruto))
      .slice(0, 3);

    return {
      melhoresPorcentagem: sortedByPorcentagem,
      melhoresValorBruto: sortedByValorBruto,
    };
  };


  const removeRepetitionEnterprise = (data) => {
    let enterprises = {}
    data.forEach(element => {
      if (!enterprises[element.enterprise]) {
        enterprises[element.enterprise] = element;
      }

    });
    return Object.values(enterprises);
  }
  const atualizarSelectedBar = (novoValor) => {
    setSelectedBar(novoValor);
  };

  const handleChangeSelect = (event) => {
    setModoOrdenacao(event.target.value);
  };


  const dataChart = dataProducts.analitycs
    ? [
      ['Empresa', 'Quantidade'],
      ...dataProducts.analitycs.map(item => [item.key, item.value > 1 ? item.value : null]).filter(item => item[1] !== null)
    ]
    : [['Empresa', 'Quantidade']]


  const chartEvents = [
    {
      eventName: 'select',
      callback({ chartWrapper }) {
        setSelectedBar(null);

        const chart = chartWrapper.getChart();
        const selection = chart.getSelection();
        if (selection.length === 0) return;

        const [selectedItem] = selection;
        const dataTable = chartWrapper.getDataTable();
        const { row } = selectedItem;
        const value = dataTable.getValue(row, 0);

        setSelectedBar(value);
      }
    }
  ]


  return (
    <div className="App">
      <h1>ML SCRAPING FRONTEND</h1>

      <div>
        <h2> Selecione uma categoria para analisar</h2>
        <select>
          {categories.map((item, index) => (
            <option key={index}>
              {item} {/* Ou qualquer outra coisa que você queira fazer com cada item */}
            </option>
          ))}

        </select>
        <h2>Empresas com maior destaque</h2>
        <div className='enterprises_first_page'>
          {dataEnterprises.map((item, index) => (
            item.enterprise &&
            <div className='enterprises_card'>{item.enterprise}</div>
          ))}
        </div>
        <h2>Melhores promoções do dia</h2>
        <select onChange={handleChangeSelect}>
          <option >Porcentagem</option>
          <option>Valor Bruto</option>
        </select>
        <div className='promotions'>
          {
            dataPromotions['melhoresPorcentagem'] && dataPromotions[modoOrdenacao === 'Porcentagem' ? 'melhoresPorcentagem' : 'melhoresValorBruto'].map((item, index) => {
              return (
                <a key={index} href={item.link} target="_blank" rel="noopener noreferrer" className='promotion-card'>
                  <h2>{item.promotion && item.promotion.porcentagem}</h2>
                  <div className='promotion-price'>
                    <h3>R$ {item.price}</h3>
                    <s>{item.promotion.valorBruto}</s>
                  </div>
                  <h4>{item.enterprise}</h4>
                  <h5 className='promotion-title'>{item.title}</h5>
                </a>
              )

            })
          }
        </div>
        <h2>Rank de empresas com produtos em Oferta</h2>
        <div className="google-chart-div" >
          <Chart
            width="100%"
            height="200vh"
            chartType="Bar"

            loader={<div>Loading Chart</div>}
            data={dataChart}
            options={{

              title: 'Rank de empresas com Ofertas!',
              hAxis: {
                title: 'Total',
                minValue: 0,
              },

              bars: "horizontal",

            }}
            chartEvents={chartEvents}
          />
          {selectedBar && <EmpresaCard atualizarSelectedBar={atualizarSelectedBar} empresaSelecionada={selectedBar} dados={dataProducts} />}
          {dataProducts.metrics ? (
            <>
              <h5>Empresas analisadas: {dataProducts.metrics.totalEnterprise} </h5>
              <h5>Produtos analisados: {dataProducts.metrics.totalProducts} </h5>
            </>
          ) : (
            <p>Loading metrics...</p>
          )}
        </div>

      </div>
      <h2>Tipos de produtos com mais promoções</h2>
      <div className='type_promotions'>
        <Chart
          width={'100%'}
          height={'300px'}
          chartType="Bar"
          loader={<div>Loading Chart</div>}
          data={[
            ['Produto', 'Quantidade'],
            ...dataProductsTypePromotion.slice(0, 10).map(item => [item[0], item[1]])
          ]}
          options={{
            title: 'Tipos de produtos mais vendidos',
            is3D: true,
          }}
          rootProps={{ 'data-testid': '1' }}
        />


      </div>
      <h2> Categoria de produtos com maior quantidade de cupom </h2>
      <h2> Análise da concorrência de um produto especifico</h2>
      <label> Insira o Link de um produto</label>

      { /* para analise empresarial qdn eu for fazer
      
      Popularidade dos produtos: Identifique os produtos mais vendidos.
Margem de lucro por produto: Compare a margem de lucro de diferentes produtos.
Análise de reviews: Analise os reviews dos produtos para identificar pontos fortes e fracos.
Satisfação do cliente: Avalie a satisfação dos clientes com os produtos.

*/}


    </div>
  );
}

export default OfertaDoDia;