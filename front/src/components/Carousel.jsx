import React from 'react'

const Carousel = ({ images = [] }) => {

    const carouselItems = images.map((item, index) => {
        return (
            <div className={"carousel-item " + (index == 0 ? "active":"")} key={item.id}>
                <img src={item.image} className="d-block w-100" title={item.title} />
            </div>
        )
    })

    return (
        <div id="carouselExample" className="carousel slide">
            <div className="carousel-inner">
                {carouselItems}
            </div>
            <button className="carousel-control-prev" type="button" data-bs-target="#carouselExample" data-bs-slide="prev">
                <span className="carousel-control-prev-icon" aria-hidden="true"></span>
                <span className="visually-hidden">Previous</span>
            </button>
            <button className="carousel-control-next" type="button" data-bs-target="#carouselExample" data-bs-slide="next">
                <span className="carousel-control-next-icon" aria-hidden="true"></span>
                <span className="visually-hidden">Next</span>
            </button>
        </div>
    )
}

export default Carousel