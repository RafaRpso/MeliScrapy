import React, { useEffect, useState } from 'react';
import './EmpresaCard.css';
import Chart from 'react-google-charts';

const EmpresaCard = ({ atualizarSelectedBar, empresaSelecionada, dados }) => {
  const [mostrarCard, setMostrarCard] = useState(true);


  const toggleCard = () => {
    setMostrarCard(!mostrarCard);
    atualizarSelectedBar(null);
  };



  if (!mostrarCard) {
    return null;
  }

  const selectedProduct = (produto) => {
    window.open(produto.link, '_blank')
  }
  const dadosKPIs = [100, 200, 300];

  const produtos = dados.query.filter(item => item.enterprise === empresaSelecionada);
  const produtosComCupom = produtos.filter(item => item.cupom["haveCupom"] === true);
  const cuponsDosProdutos = produtosComCupom
    .map(item => item.cupom["cupom"])
    .filter((cupom, index, array) => array.indexOf(cupom) === index);
  const produtosComFull = produtos.filter(item => item.isFull === true);
  const produtosSemFull = produtosComFull.length - produtos.length;

  return (
    <div className='escurecer'>
      <div className="empresa-card">
        <div className="fechar-card" onClick={toggleCard}>
          X
        </div>
        <h1>{empresaSelecionada}</h1>

        <h2>Análise de Dados</h2>

        {/*
        Análise de Cupons:

    Quantidade de cupom por produto
    
    Avalie a proporção de produtos que estão marcados como "isFull" e como isso pode influenciar as vendas.

        Compare o desempenho de diferentes empresas em termos de preços e popularidade.
    Avalie se há uma correlação entre a empresa e a presença de cupons. (empresa com mais cupons )
  */}
        <div className='kpis'>
          <h3> {Math.floor((produtosComFull.length / produtos.length) * 100, 2)}% coberto pelo Full</h3>
          <h3> {Math.floor((produtosComCupom.length / produtos.length) * 100, 2)}% coberto por cupom</h3>
               {/* Adicione aqui os gráficos correspondentes aos KPIs */}
        </div>
        <hr></hr>
        <div className='cupom'>
          <h2>Cupons</h2>
          <div className='cupom-lista'>
            {cuponsDosProdutos.map((cupom, index) => (
              <div key={index} className='cupom-card'>
                {cupom}
              </div>
            ))}
          </div>

        </div>

        {/* Lista de produtos */}
        {/* Tabela de produtos */}
        <div className='table'>
          <h3>Produtos</h3>
          <table className="tabela-produtos">
            <thead>
              <tr>
                <th>Produto</th>
                <th>Preço</th>
                <th>Imagem</th>
              </tr>
            </thead>
            <tbody>
              {produtos.map((produto, index) => (
                <tr key={index} onClick={() => selectedProduct(produto)} className="produto-row">
                  <td>{produto.title}</td>
                  <td>R${produto.price}</td>
                  <td><img className="image-product" src={produto.imageUrl} alt={produto.title} /></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div></div >

  );
};

export default EmpresaCard;

