import re
import unicodedata
import urllib, urllib2
import urlparse
import cgi
import cookielib
from htmlentitydefs import name2codepoint

verbose = True
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.8.1.3) Gecko/20070309 Firefox/2.0.0.3'

def scrape(pattern, html=None, url=None, get=None, post=None, headers=None, cookie_jar=None):
	if type(pattern) == str:
		pattern = compile(pattern)
	return pattern.scrape(html, url, get, post, headers, cookie_jar)
	
def compile(pattern):
	return _Pattern(_compile(pattern, True))
	
def fetch_html(url, get=None, post=None, headers=None, cookie_jar=None):
	if get:
		if type(get) == str:
			get = cgi.parse_qs(get)
		l = list(urlparse.urlparse(url))
		g = cgi.parse_qs(l[4])
		g.update(get)
		l[4] = urllib.urlencode(g)
		url = urlparse.urlunparse(l)
	if post and type(post) != str:
		post = urllib.urlencode(post)
	if cookie_jar == None:
		cookie_jar = cookielib.CookieJar()
	if not headers:
		headers = {'User-Agent': user_agent}
	else:
		if 'User-Agent' not in headers:
			headers['User-Agent'] = user_agent
	if verbose:
		print 'fetching', url, '...'
	request = urllib2.Request(url, post, headers)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie_jar))
	res = opener.open(request).read()
	if verbose:
		print 'DONE fetching.'
	return res


# INTERNALS
# ----------------------------------------------------------------------

class _Pattern:

	def __init__(self, nodes):
		self._nodes = nodes
	
	def scrape(self, html=None, url=None, get=None, post=None, headers=None, cookie_jar=None):
		if cookie_jar == None:
			cookie_jar = cookielib.CookieJar()
		if html == None:
			html = fetch_html(url, get, post, headers, cookie_jar)
		captures = {}
		if _match(self._nodes, _remove_comments(html), 0, captures, url, cookie_jar) == -1:
			return None
		if len(captures) == 1 and '' in captures:
			return captures['']
		return captures
		

# node types     # information in tuple
_TEXT = 1        # (_TEXT, regex)
_TAG = 2         # (_TAG, open_regex, close_regex, attributes, children)   attributes {name: (regex, special_nodes) ...}
_CAPTURE = 3     # (_CAPTURE, name_parts, filters)
_SCAN = 4        # (_SCAN, children)
_GOTO = 5        # (_GOTO, filters, children)

_space_re = re.compile(r'\s+')
_tag_re = re.compile(r'<[^>]*>')
_attr_re = re.compile(r'([\w-]+)(?:\s*=\s*(?:(["\'])(.*?)\2|(\S+)))?', re.S)
_attr_start_re = re.compile(r'([\w-]+)(?:\s*=\s*)?')
_comment_re = re.compile(r'<!--.*?-->', re.S)
_script_re = re.compile(r'<script[^>]*>.*?</script>', re.S | re.I)
_entity_re = re.compile("&(#?)(\d{1,5}|\w{1,8});")
_closure_start_re = re.compile(r'<|\{[\{\*\@\#]')
_capture_list_re = re.compile(r'\[(\w*)\]')


# functions for compiling a pattern into nodes
# --------------------------------------------------------------

def _compile(s, re_compile):
	slen = len(s)
	i = 0
	nodes = []
	stack = []
	while i < slen:
		m = _closure_start_re.search(s, i)
		if not m:
			break
		closure_name = m.group(0)
		# text since last closure
		text = s[i:m.start()].strip()
		if text:
			nodes.append((_TEXT, _make_text_re(text, re_compile)))
		i = m.end()
		# an HTML tag
		if closure_name == '<':
			inner, i = _next_closure(s, i, '<', '>')
			inner = inner.strip()
			if inner:
				# end tag
				if inner[0] == '/':
					if stack:
						nodes = stack.pop()
				# standalone tag
				elif inner[-1] == '/':
					l = inner[:-1].split(None, 1)
					name = l[0].strip()
					attrs = {} if len(l) == 1 else _compile_attrs(l[1], re_compile)
					nodes.append((_TAG, _make_start_tag_re(name, re_compile), _make_end_tag_re(name, re_compile), attrs, []))
				# start tag
				else:
					l = inner.split(None, 1)
					name = l[0].strip()
					attrs = {} if len(l) == 1 else _compile_attrs(l[1], re_compile)
					new_nodes = []
					nodes.append((_TAG, _make_start_tag_re(name, re_compile), _make_end_tag_re(name, re_compile), attrs, new_nodes))
					stack.append(nodes)
					nodes = new_nodes
		# special brackets
		else:
			special_type = closure_name[1]
			# capture
			if special_type == '{':
				inner, i = _next_closure(s, i, '{{', '}}')
				nodes.append(_compile_capture(inner))
			# scan
			elif special_type == '*':
				inner, i = _next_closure(s, i, '{*', '*}')
				nodes.append((_SCAN, _compile(inner, re_compile)))
			# goto
			elif special_type == '@':
				inner, i = _next_closure(s, i, '{@', '@}')
				if inner:
					filters = []
					if inner[0] == '|':
						filters, inner = (inner.split(None, 1) + [''])[:2]
						filters = filters.split('|')[1:]
					nodes.append((_GOTO, filters, _compile(inner, True)))
			# comment
			elif special_type == '#':
				i = s.find('#}')
				if i == -1:
					break
				i += 2
	# ending text
	text = s[i:].strip()
	if text:
		nodes.append((_TEXT, _make_text_re(text, re_compile)))
	stack.append(nodes)
	return stack[0]
	
def _compile_capture(s): # returns the tuple with _CAPTURE
	filters = s.strip().split('|')
	name = filters.pop(0)
	name_parts = []
	for part in name.split('.'):
		m = _capture_list_re.match(part)
		if m:
			name_parts.append((m.group(1),))
		else:
			name_parts.append(part)
	return (_CAPTURE, name_parts, filters)
	
def _compile_attrs(s, re_compile):
	attrs = {}
	i = 0
	slen = len(s)
	while i < slen:
		m = _attr_start_re.search(s, i)
		if not m:
			break
		name = m.group(1).lower()
		i = m.end()
		if i >= slen:
			break
		quote = s[i]
		# no quotes, value ends at next whitespace
		if quote != '"' and quote != "'":
			m = _space_re.search(s, i)
			if m:
				val = s[i:m.start()]
				i = m.end()
			else:
				val = s[i:]
				i = slen
		# quotes
		else:
			i += 1
			start = i
			# find the ending quote, skipping over { }
			while i < slen:
				quote_i = s.find(quote, i)
				bracket_i = s.find('{', i)
				if quote_i == -1:
					i = slen
					break
				elif bracket_i == -1 or quote_i < bracket_i:
					i = quote_i
					break
				else:
					inner, i = _next_closure(s, bracket_i + 1, '{', '}')
			val = s[start:i]
		val = val.strip()
		regex = ''
		special_nodes = []
		if val: # if there is no value, empty regex string won't be compiled
			nodes = _compile(val, False)
			# concatenate regexes
			for node in nodes:
				if node[0] == _TEXT:
					regex += node[1]
				elif node[0] != _TAG:
					regex += '(.*)'
					special_nodes.append(node)
			if regex != '(.*)':
				regex = '(?:^|\s)' + regex + '(?:\s|$)' # match must be flush with whitespace or start/end
			if re_compile:
				regex = re.compile(regex, re.I)
		attrs[name] = (regex, special_nodes)
	return attrs
	
def _make_start_tag_re(name, re_compile):
	regex = r'<\s*' + re.escape(name) + r'(?:\s+([^>]*)|(\s*\/))?>'
	if re_compile:
		regex = re.compile(regex, re.I)
	return regex
	
def _make_end_tag_re(name, re_compile):
	regex = r'</\s*' + re.escape(name) + r'\s*>'
	if re_compile:
		regex = re.compile(regex, re.I)
	return regex
	
def _make_text_re(text, re_compile):
	regex = r'\s+'.join([re.escape(w) for w in text.split()])
	if re_compile:
		regex = re.compile(regex, re.I)
	return regex
	
	
# functions for running pattern nodes on html
# ---------------------------------------------------------------

def _match(nodes, html, i, captures, base_url, cookie_jar): # returns substring index after match, -1 if no match
	anchor_i = i
	special = []
	for node in nodes:
		# match text node
		if node[0] == _TEXT:
			m = node[1].search(html, i)
			if not m:
				return -1
			# run previous special nodes
			if not _run_special_nodes(special, html[anchor_i:m.start()], captures, base_url, cookie_jar):
				return -1
			special = []
			i = anchor_i = m.end()
		# match html tag
		elif node[0] == _TAG:
			while True:
				# cycle through tags until all attributes match
				while True:
					m = node[1].search(html, i)
					if not m:
						return -1
					i = m.end()
					attrs = _parse_attrs(m.group(1) or '')
					attrs_matched = _match_attrs(node[3], attrs, captures, base_url, cookie_jar)
					if attrs_matched == -1:
						return -1
					if attrs_matched:
						break
				if m.group(2): # standalone tag
					break
				else: # make sure children match
					body, i = _next_tag(html, i, node[1], node[2])
					nested_captures = {}
					if _match(node[4], body, 0, nested_captures, base_url, cookie_jar) != -1:
						_merge_captures(captures, nested_captures)
						break
			# run previous special nodes
			if not _run_special_nodes(special, html[anchor_i:m.start()], captures, base_url, cookie_jar):
				return -1
			special = []
			anchor_i = i
		else:
			special.append(node)
	if not _run_special_nodes(special, html[i:], captures, base_url, cookie_jar):
		return -1
	return i
		
def _match_attrs(attr_nodes, attrs, captures, base_url, cookie_jar): # returns True/False, -1 if failed _run_special_node
	for name, attr_node in attr_nodes.items():
		if name not in attrs:
			return False
		if attr_node[0]: # if attr_node[0] is empty string, done matching
			m = attr_node[0].match(attrs[name])
			if not m:
				return False
			# run regex captures over parallel list of special nodes
			for i, special_node in enumerate(attr_node[1]):
				if not _run_special_node(special_node, m.group(i+1), captures, base_url, cookie_jar):
					return -1
	return True

def _run_special_nodes(nodes, s, captures, base_url, cookie_jar): # returns True/False
	for node in nodes:
		if not _run_special_node(node, s, captures, base_url, cookie_jar):
			return False
	return True
		
def _run_special_node(node, s, captures, base_url, cookie_jar): # returns True/False
	if node[0] == _CAPTURE:
		s = _apply_filters(s, node[2], base_url)
		_set_capture(captures, node[1], s)
	elif node[0] == _SCAN:
		i = 0
		while True:
			nested_captures = {}
			i = _match(node[1], s, i, nested_captures, base_url, cookie_jar)
			if i == -1:
				break
			else:
				_merge_captures(captures, nested_captures)
		# scan always ends with an usuccessful match, so fill in captures that weren't set
		_fill_captures(node[1], captures)
	elif node[0] == _GOTO:
		new_url = _apply_filters(s, node[1] + ['abs'], base_url)
		new_html = fetch_html(new_url, cookie_jar=cookie_jar)
		if _match(node[2], new_html, 0, captures, new_url, cookie_jar) == -1:
			return False
	return True
	
def _set_capture(captures, name_parts, val, list_append=True):
	obj = captures
	last = len(name_parts) - 1
	for i, part in enumerate(name_parts):
		if i == last:
			new_obj = val
		else:
			new_obj = {}
		if type(part) == tuple:
			if part[0] not in obj:
				if list_append:
					obj[part[0]] = [new_obj]
				else:
					obj[part[0]] = []
					break
			else:
				if type(obj[part[0]]) != list:
					break
				if i == last or len(obj[part[0]]) == 0 or name_parts[i+1] in obj[part[0]][-1]:
					if list_append:
						obj[part[0]].append(new_obj)
					else:
						break
				else:
					new_obj = obj[part[0]][-1]
		else:
			if part not in obj:
				obj[part] = new_obj
			else:
				new_obj = obj[part]
		obj = new_obj
		
def _merge_captures(master, slave):
	for name, val in slave.items():
		if name not in master:
			master[name] = val
		else:
			if type(val) == dict and type(master[name]) == dict:
				_merge_captures(master[name], val)
			elif type(val) == list and type(master[name]) == list:
				for e in val:
					if type(e) == dict:
						for n, v in e.items():
							if len(master[name]) == 0 or type(master[name][-1]) != dict or n in master[name][-1]:
								master[name].append({n: v})
							else:
								master[name][-1][n] = v
					else:
						master[name].append(e)
		
def _fill_captures(nodes, captures):
	for node in nodes:
		if node[0] == _TAG:
			_fill_captures(node[4], captures)
			for attr in node[3].values():
				_fill_captures(attr[1], captures)
		elif node[0] == _CAPTURE:
			_set_capture(captures, node[1], _apply_filters(None, node[2], None), False)
		elif node[0] == _SCAN:
			_fill_captures(node[1], captures)
		elif node[0] == _GOTO:
			_fill_captures(node[2], captures)
		
def _apply_filters(s, filters, base_url):
	if 'html' not in filters and issubclass(type(s), basestring):
		s = _remove_html(s)
	for f in filters:
		if f == 'unescape':
			if issubclass(type(s), basestring):
				s = s.decode('string_escape')
		elif f == 'abs':
			if issubclass(type(s), basestring):
				s = urlparse.urljoin(base_url, s)
		elif f == 'int':
			try:
				s = int(s)
			except:
				s = 0
		elif f == 'float':
			try:
				s = float(s)
			except:
				s = 0.0
		elif f == 'bool':
			s = bool(s)
	return s
	
	
# html/text utilities
# ---------------------------------------------------------------

def _remove_comments(s):
    return _comment_re.sub('', s)

def _remove_html(s):
	s = _comment_re.sub('', s)
	s = _script_re.sub('', s)
	s = _tag_re.sub('', s)
	s = _space_re.sub(' ', s)
	s = _decode_entities(s)
	s = s.strip()
	return s
	
def _decode_entities(s):
	if type(s) is not unicode:
		s = unicode(s, 'utf-8', 'ignore')
		s = unicodedata.normalize('NFKD', s)
	return _entity_re.sub(_substitute_entity, s)
	
def _substitute_entity(m):
	ent = m.group(2)
	if m.group(1) == "#":
		return unichr(int(ent))
	else:
		cp = name2codepoint.get(ent)
		if cp:
			return unichr(cp)
		else:
			return m.group()
			
def _parse_attrs(s):
	attrs = {}
	for m in _attr_re.finditer(s):
		attrs[m.group(1)] = m.group(3) or m.group(4)
	return attrs
	
def _next_tag(s, i, tag_open_re, tag_close_re, depth=1): # returns (tag body, substring index after tag)
	slen = len(s)
	start = i
	while i < slen:
		tag_open = tag_open_re.search(s, i)
		tag_close = tag_close_re.search(s, i)
		if not tag_close:
			i = len(s)
			break
		elif not tag_open or tag_close.start() < tag_open.start():
			i = tag_close.end()
			depth -= 1
			if depth == 0:
				return s[start:tag_close.start()], i
		else:
			if not (tag_open and tag_open.group(2)): # not a standalone tag
				depth += 1
			i = tag_open.end()
	return s[start:i], i

def _next_closure(s, i, left_str, right_str, depth=1): # returns (closure body, substring index after closure)
	slen = len(s)
	start = i
	while i < slen:
		left = s.find(left_str, i)
		right = s.find(right_str, i)
		if right == -1:
			i = len(s)
			break
		elif left == -1 or right < left:
			i = right + len(right_str)
			depth -= 1
			if depth == 0:
				return s[start:right], i
		else:
			depth += 1
			i = left + len(left_str)
	return s[start:i], i
	
