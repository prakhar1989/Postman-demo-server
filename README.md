PostmanBin
===

Demo server for testing / demonstrating Postman. Postman collection with the api endpoints can be downloaded [here](https://www.getpostman.com/collections/fc3f0598daaa5271e4f7).

### Build Steps 

Make sure you have `sqlite` installed.

   $ git clone https://github.com/prakhar1989/Postman-demo-server.git 
   $ virtualenv venv 
   $ source venv/bin/activate
   $ pip install -r requirements.txt
   $ python setup.py # sets up the database
   $ python app.py 
    * Running on http://127.0.0.1:5000/
    * Restarting with reloader

To deploy a flask app I have a blogpost written [here](http://prakhar.me/articles/flask-on-nginx-and-gunicorn/) which you can follow.

### Endpoints

<table>
<thead>
<tr>
	<th></th>
	<th>Method</th>
	<th>Endpoint</th>
	<th>Description</th>
</tr>
</thead>
<tbody>
<tr>
   <th>1</th>
   <th>GET</th>
   <th>{{url}}/blog/posts</th>
   <th>Return all blog posts</th>
</tr>
<tr>
   <th>2</th>
   <th>DELETE</th>
   <th>{{url}}/blog/posts/{{id}}</th>
   <th>Delete the existing blog post</th>
</tr>
<tr>
   <th>3</th>
   <th>GET</th>
   <th>{{url}}</th>
   <th>Returns a JSON with all the available API endpoints.</th>
</tr>
<tr>
   <th>4</th>
   <th>GET</th>
   <th>{{url}}/blog/users/{{user_id}}</th>
   <th>Get user details for a user</th>
</tr>
<tr>
   <th>5</th>
   <th>GET</th>
   <th>{{url}}/blog/posts/{{id}}</th>
   <th>Return blog post with that ID</th>
</tr>
<tr>
   <th>6</th>
   <th>POST</th>
   <th>{{url}}/blog/users/</th>
   <th>Create a new user with the given username and password.</th>
</tr>
<tr>
   <th>7</th>
   <th>POST</th>
   <th>{{url}}/blog/posts</th>
   <th>Create a new blog post</th>
</tr>
<tr>
   <th>8</th>
   <th>GET</th>
   <th>{{url}}/cookies/delete?name</th>
   <th>Similar to httpbin.org/cookies. Delete a cookie.</th>
</tr>
<tr>
   <th>9</th>
   <th>GET</th>
   <th>{{url}}/delay/10</th>
   <th>Return response after a few seconds</th>
</tr>
<tr>
   <th>10</th>
   <th>POST</th>
   <th>{{url}}/post</th>
   <th>Similar to httpbin.org/post. Return POST data.</th>
</tr>
<tr>
   <th>11</th>
   <th>POST</th>
   <th>{{url}}/blog/users/tokens/</th>
   <th>POST on this endpoint will create a new token provided the username and password is correct. The returned token will be used to make subsequent requests.</th>
</tr>
<tr>
   <th>12</th>
   <th>GET</th>
   <th>{{url}}/cookies</th>
   <th>Similar to httpbin.org/cookies. Return cookies set in the domain.</th>
</tr>
<tr>
   <th>13</th>
   <th>DELETE</th>
   <th>{{url}}/blog/users/tokens/{{token_id}}</th>
   <th>Delete the token. Effectively signing out the user.</th>
</tr>
<tr>
   <th>14</th>
   <th>GET</th>
   <th>{{url}}/get</th>
   <th>Similar to httpbin.org/get. Return GET data.</th>
</tr>
<tr>
   <th>15</th>
   <th>GET</th>
   <th>{{url}}/headers</th>
   <th>Similar to httpbin.org/headers. Return all the headers passed to it.</th>
</tr>
<tr>
   <th>16</th>
   <th>GET</th>
   <th>{{url}}/cookies/set?name=value</th>
   <th>Similar to httpbin.org/cookies. Set a cookie</th>
</tr>
<tr>
   <th>17</th>
   <th>PUT</th>
   <th>{{url}}/blog/posts/{{id}}</th>
   <th>Modify the existing post</th>
</tr>
<tr>
   <th>18</th>
   <th>GET</th>
   <th>{{url}}/blog/users/</th>
   <th>Get all current users of the blog.</th>
</tr>
<tr>
   <th>19</th>
   <th>GET</th>
   <th>{{url}}/status</th>
   <th>Return the status of the API with the timestamp.</th>
</tr>    
</tbody>
</table>

### Thanks 
[HTTPBIN](http://httpbin.org) for inspiration
