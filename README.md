<h1> API Tracker Solution</h1>

<h2>Objective</h2>
    <p>Create a Solution to serverless to know where the drivers trucker has been and where they are sleeping or just stopping the truck.</p>

<h2>Insights or hypotheses</h2>
    <p>where the best place to offer products?</p>
    <p>Where the best place to build a base structure the place to rest, fuel, and take a shower?</p>
    <p>where they most stop to fuel diesel?</p>
    <p>what the most common routes?</p>
    <p>what time is the top flow?</p>
    <p>What demand space for attending their necessities?</p>
    <p>How many liters of diesel will be necessary in each place?</p>
    <p>Prediction of demands in each base with machine learning</p>

<h3>How</h3>
    <li>Request from Tracker API to object</li>
    <li>Transform data from json with pandas to DataFrame</li>
    <li>Insertion database sqlite from DataFrame</li>
    <li>Create a routine every 30 minutes to store data</li>
    <li>Create the API with Flask</li>
    <li>Create a dashboard with streamlit to show and interaction information, with charts, tables, maps, heatmap, etc</li>

<h3>Guide Project</h3>
<p>Do you have following files: </p>
    <li>notebook_tracker.ipynb</li> this file it's to understand all code solution on mind
    <li>create_table.py</li>
    It's to run only one time
    <li>request_api.py</li>
    This is to request from API and data preparation and selection
