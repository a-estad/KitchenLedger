const Form = ({addDinnerclub, newDinnerclub, handleInputChange}) => {
    return (
        <form onSubmit={addDinnerclub}>
            <div>
                <label>Description:</label>
                <input
                    type="text"
                    name="description"
                    value={newDinnerclub.description}
                    onChange={handleInputChange}
                    required
                />
            </div>
            <div>
                <label>Cost:</label>
                <input
                    type="number"
                    name="cost"
                    value={newDinnerclub.cost}
                    onChange={handleInputChange}
                    required
                />
            </div>
            <div>
                <label>Date:</label>
                <input
                    type="date"
                    name="date"
                    value={newDinnerclub.date}
                    onChange={handleInputChange}
                    required
                />
            </div>
            <button type="submit">Create Dinnerclub</button>
        </form>
    )
}

export default Form