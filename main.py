from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:Mendali4@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(5000))

    def __init__(self, title, body, id):
        self.title = title
        self.body = body
        self.id = id

@app.route('/newpost', methods=['POST','GET'])
def post_blog():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        Error = False
        error = {
            'title' : '',
            'body' : ''
        }

        if (title == ""):
            error['title'] = "Please enter a title."
            Error = True
            pass
        else:
            pass
        
        if (body == ""):
            error['body'] = "Please enter a blog."
            Error = True
            pass
        else:
            pass

        if (Error == True):
            return render_template('newpost.html', title=title, body=body, error=error)
        else:
            new_post= Blog(title, body)
            db.session.add(new_post)
            db.session.commit()

            blog = {
                'title' : title,
                'body' : body
            }
            
            return render_template('post.html', blog=blog)

    return render_template('newpost.html')

@app.route('/blog')
def disp_blog():
    #Now that I've clicked on a blog entry from the main page's list I have an ID that I want to retrieve. How do I query my database to get just that id as an object to pass into post.html?
    blog_id = request.args.get('id')
    blog = Blog.query.get(blog_id)
    
    return render_template('post.html', blog=blog)

@app.route('/', methods=['POST','GET'])
def index():

    blog = Blog.query.all()
    encoded_error = request.args.get('error')

    return render_template('blog.html', blog=blog, error=encoded_error and cgi.escape(encoded_error, quote=True))

if __name__ == '__main__':
    app.run()