import React, { useEffect, useState } from 'react'
import Carousel from './components/Carousel'
import UploadImageModal from './components/UploadImageModal'

const App = () => {

    const [gallery, setGallery] = useState([])
    const [show, setShow] = useState(false)

    useEffect(() => {
        getGallery()
    }, [])

    const getGallery = async () => {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/gallery')
            const data = await response.json()
            setGallery(data)
        } catch (error) {
            console.log(error.message)
        }
    }

    const uploadImage = async (formData) => {

        try {

            const response = await fetch('http://127.0.0.1:5000/api/upload', {
                method: 'POST',
                body: formData
            })

            const data = await response.json()
            if(data.id){
                getGallery()
            }
            return data
            
        } catch (error) {
            console.log(error.message)
        }

    }

    return (
        <>
            <div className="container-fluid">
                <div className="row">
                    <div className="col-md-12 g-0">
                        <Carousel images={gallery} />
                    </div>
                </div>
            </div>
            <button className="btn btn-primary btn-sm my-3" onClick={() => setShow(!show)}>Upload Image</button>
            <UploadImageModal show={show} setShow={setShow} uploadImage={uploadImage} />
        </>
    )
}

export default App