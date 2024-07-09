import React from 'react';
import { useState } from 'react';
import './avaliacao.css';

function MyAvaliacao() {
    const [productLink, setProductLink] = useState('');
    const [ratings, setRatings] = useState([]);
    const [responses, setResponses] = useState(Array(ratings.length).fill(''));



    const verifyIfProductLinkIsValid = (link) => {
        if (link.includes('https://www.mercadolivre.com.br/')) {
            return true;
        }
        else {
            return false;
        }

    }
    const getRatings = async () => {
        if (!verifyIfProductLinkIsValid(productLink)) {
            return alert("Link inválido")
        }
        await fetch(`http://localhost:5000/questions/${productLink}`,)
            .then(response => response.json())
            .then(data => {
                setRatings(data);

            });
    }

    const gptResponse = async (currentRating, index) => {
        console.log(currentRating)
        const productId = currentRating.product_id;
        const questionText = currentRating.question.text;

        await fetch(`http://localhost:5000/product/${productId}`).then(response => response.json()).then(data => {
            console.log(data)
            const productData = data.recommended_products[0];
            const productDetails = productData.product_details

            const query = `Preciso que responda um chamado, a partir de agora foque somente em responde-lo, não aja como uma inteligência artificial e sim como um ser humano. 
            
            O cliente está perguntando sobre o produto "${productData.name}" e a pergunta é: "${questionText}"

            Os detalhes necessários para você responder podem vir de uma pesquisa interna sua ou baseada nesses dados (estão em JSON, mas converta para linguagem natural quando responder o chamado):
            ${JSON.stringify(productDetails)}
            
            
            Ao final, responda o chamado com a resposta que você achar mais adequada, gentil e sutil. Estou te utilizando para cumprir o temp ode SLA do chamado.
    
            Tente escrever no máximo até 5 linhas, não se exceda. Dê bom dia, boa tarde ou boa noite, dependendo do horário. Seja gentil e educado. Seja humano.
            `

            fetch(`http://localhost:5000/gpt3`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    query: query
                })
            }).then(response => response.json()).then(data => {

                const newResponses = [...responses];
                console.log(data)
                newResponses[index] = data.choices[0].message.content;
                setResponses(newResponses);



            })
        })
    }

    return (
        <div className="container">
            <h1 className="title">Avaliações</h1>
            <button className="mass-recommendation-btn">Recomendação em massa</button>
            <h3 className="subtitle">Insira o link de um produto</h3>
            <div className="input-container">
                <input
                    placeholder="Link produto do mercado livre"
                    type="text"
                    id="search"
                    name="search"
                    value={productLink}
                    onChange={(e) => setProductLink(e.target.value)}
                />
                <button className="confirm-btn" onClick={getRatings}>
                    Confirmar
                </button>
            </div>

            <div className='ratings'>
                {ratings.map((rating, index) => (
                    <div className='card-rating' key={index}>
                        <p>{rating.question_date_formatted}</p>
                        <h4>{rating.question.text}</h4>
                        <button onClick={() => gptResponse(rating, index)}>Sugestão de resposta por IA</button>
                        <div className='ia-response' id={index}>
                            {responses[index]}
                        </div>
                    </div>
                ))}
            </div>

        </div>
    );
}

export default MyAvaliacao;
