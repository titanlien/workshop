require 'sinatra'

get '/' do
  "hello world! it's #{Time.now} here!"
end
