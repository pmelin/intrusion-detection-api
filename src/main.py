from prometheus_fastapi_instrumentator.metrics import Info
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from predict import predict


def intrusion_prediction_results_total():
    """
    Sets up the custom metric intrusion_prediction_results_total to be captured by 
    prometheus_fastapi_instrumentator
    """
    METRIC = Counter(
        "intrusion_prediction_results_total",   
        "Intrusion Prediction Results",
        labelnames=("is_intrusion",))

    def instrumentation(info: Info) -> None:
        if "x-is-intrusion" in info.response.headers: 
            is_intrusion_result = info.response.headers["x-is-intrusion"]
            METRIC.labels(is_intrusion_result).inc()

    return instrumentation

# Sets up the app and the dingle POST route

app = FastAPI()

# allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post('/is_intrusion')
async def is_intrusion(request: Request, response: Response):
    """
    Method that handles the HTTP Post with the data to be evaluated
    if it's an intrusion.
    """

    # loads the request body as json
    body = await request.json()

    # predicts if the data from the body is an intrusion
    is_intrusion = predict(body)

    # saves the result on a header to allow us to get it on 
    # the instrumentation function
    response.headers["x-is-intrusion"] = str(is_intrusion)

    # returns the response
    return {
        "is_intrusion": is_intrusion
    }



# instruments the app to make metrics available to prometheus
instrumentator = Instrumentator()
instrumentator.add(intrusion_prediction_results_total())
instrumentator.instrument(app).expose(app)
