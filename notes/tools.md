# Sudoers

Tools and their specific usage:

#cewl

- creating a list of emails from a certain website `cewl -e --email_file emails http://sneakycorp.htb/`

#Evolution

- email client which allows you to select the mail server too. Thus, boxes like `sneaky mailer` used this.

- evolution allows setting server and port for SMTP and IMAP (other services as well); and a lot of other things as well like TLS things.

# Jackson Deserialization vulnerability

[Link](https://medium.com/@swapneildash/understanding-insecure-implementation-of-jackson-deserialization-7b3d409d2038)

- a java library used to interconvert between POJO (Plain old java objects) and JSON. It serializes POJO to JSON, and deserializes JSON to POJO.

```s
public class MyValue {
    public String name;
    public int age;
}

//deserialization class

ObjectMapper om = new ObjectMapper();

MyValue myvalue = om.readValue(Files.readAllBytes(Paths.get("**.json")), MyValue.class);

//PenetrationTesting 

pt = om.readValue(Files.readAllBytes(Paths.get("***.json")), PenetrationTesting.class);
```

`ObjectMapper`: class in Jackson that lets deserialize a JSON to a java object. It reads from a file and creates an object of the class `MyValue`. For instance, the input `{"name":"testname","age":12}` will create an object of class `MyValue` with the attribute `name` set to `testname` and `age` to `12`.

In short, this allows you to host an infected payload somewhere, and call a Java gadget to do things.

- JSON starting with **{** is JSON object.

- JSON starting with **[** is JSON array.

