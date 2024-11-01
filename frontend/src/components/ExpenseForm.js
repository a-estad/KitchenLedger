const Form = ({addExpense, newExpense, handleInputChange}) => {
    return (
        <form onSubmit={addExpense}>
            <div>
                <label>Description:</label>
                <input
                    type="text"
                    name="description"
                    value={newExpense.description}
                    onChange={handleInputChange}
                    required
                />
            </div>
            <div>
                <label>Cost:</label>
                <input
                    type="number"
                    name="cost"
                    value={newExpense.cost}
                    onChange={handleInputChange}
                    required
                />
            </div>
            <div>
                <label>Date:</label>
                <input
                    type="date"
                    name="date"
                    value={newExpense.date}
                    onChange={handleInputChange}
                    required
                />
            </div>
            <button type="submit">Create Expense</button>
        </form>
    )
}

export default Form