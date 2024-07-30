export function TransferDone (){
    return (
        <div className="flex justify-center h-screen bg-gray-100">
            <div className="h-full flex flex-col justify-center">
                <div className="border h-min text-card-foreground max-w-md p-4 space-y-8 w-96 bg-white shadow-lg rounded-lg">
                    <div className="flex flex-col space-y-1.5 p-6">
                        <h2 className="text-3xl font-bold text-center">Success</h2>
                    </div>
                    <div className="p-6">
                        <div className="text-green-500 text-2xl text-center">
                        <h1>Transfer Done Succesfully</h1>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}