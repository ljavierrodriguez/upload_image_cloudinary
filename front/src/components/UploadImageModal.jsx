import React, { useState } from 'react'

const UploadImageModal = ({ show, setShow, uploadImage }) => {

    const [title, setTitle] = useState('')
    const [image, setImage] = useState(null)

    const handleSubmit = async (e) => {
        e.preventDefault()

        const formData = new FormData()

        formData.append("title", title)
        formData.append("image", image)

        const resp = await uploadImage(formData)

        if (resp.id) {
            e.target.reset()
            setTitle('')
            setImage(null)
            setShow(!show)
        }
    }

    return (
        <div className={`modal fade ${(show ? "show" : "")}`} style={{ display: show ? "block" : "none" }} id="exampleModal" tabIndex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div className="modal-dialog">
                <div className="modal-content">
                    <form onSubmit={handleSubmit}>
                        <div className="modal-header">
                            <h1 className="modal-title fs-5" id="exampleModalLabel">Modal title</h1>
                            <button type="button" className="btn-close" data-bs-dismiss="modal" aria-label="Close" onClick={() => setShow(!show)}></button>
                        </div>
                        <div className="modal-body">
                            <div className="row">
                                <div className="form-group col-12">
                                    <label htmlFor="title" className="form-label">Title:</label>
                                    <input type="text" id="title" className="form-control" placeholder='title' onChange={(e) => setTitle(e.target.value)} />
                                </div>
                                <div className="form-group col-12">
                                    <label htmlFor="image" className="form-label">Image</label>
                                    <input type="file" id="image" className="form-control" accept='.jpg,.png,.gif,.jpeg' onChange={(e) => setImage(e.target.files[0])} />
                                </div>
                            </div>
                        </div>
                        <div className="modal-footer">
                            <button type="button" className="btn btn-secondary" data-bs-dismiss="modal" onClick={() => setShow(!show)}>Close</button>
                            <button type="submit" className="btn btn-primary">Save changes</button>
                        </div>
                    </form>
                </div>
            </div>
        </div >
    )
}

export default UploadImageModal