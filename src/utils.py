def get_params(args):
    args = args.to_dict()
    params = ['dureza', 'tasaprod', 'calidad']

    if len(args) == 3 and list(args.keys()) == params:
        try:
            hardness = round(float(args[params[0]]), 3)
            prod_rate = round(float(args[params[1]]), 3)
            quality = round(float(args[params[2]]), 3)
        
            return hardness, prod_rate, quality

        except:
            raise SyntaxError("Values of parameters aren't valid. Only int or float type are allowed. Read API docs.")

    else:
        raise SyntaxError("Parameters are missing or not allowed. Read API docs.")