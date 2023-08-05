#!/usr/bin/env python3
# This file is a part of marzer/poxy and is subject to the the terms of the MIT license.
# Copyright (c) Mark Gillard <mark.gillard@outlook.com.au>
# See https://github.com/marzer/poxy/blob/master/LICENSE for the full license text.
# SPDX-License-Identifier: MIT

try:
	from poxy.utils import *
	import poxy.project as project
	import poxy.doxygen as doxygen
	import poxy.soup as soup
	import poxy.fixers as fixers
except:
	from utils import *
	import project
	import doxygen
	import soup
	import fixers

import os
import subprocess
import concurrent.futures as futures
import argparse
import tempfile
from lxml import etree
from io import BytesIO



#=======================================================================================================================
# PRE/POST PROCESSORS
#=======================================================================================================================

_doxygen_overrides  = (
		(r'ALLEXTERNALS',			False),
		(r'ALLOW_UNICODE_NAMES',	False),
		(r'ALWAYS_DETAILED_SEC',	False),
		(r'AUTOLINK_SUPPORT',		True),
		(r'BUILTIN_STL_SUPPORT',	False),
		(r'CASE_SENSE_NAMES',		False),
		(r'CLASS_DIAGRAMS',			False),
		(r'CPP_CLI_SUPPORT',		False),
		(r'CREATE_SUBDIRS',			False),
		(r'DISTRIBUTE_GROUP_DOC',	False),
		(r'DOXYFILE_ENCODING',		r'UTF-8'),
		(r'ENABLE_PREPROCESSING',	True),
		(r'EXCLUDE_SYMLINKS', 		False),
		(r'EXPAND_ONLY_PREDEF', 	False),
		(r'EXTERNAL_GROUPS', 		False),
		(r'EXTERNAL_PAGES', 		False),
		(r'EXTRACT_ANON_NSPACES',	False),
		(r'EXTRACT_LOCAL_CLASSES',	False),
		(r'EXTRACT_LOCAL_METHODS',	False),
		(r'EXTRACT_PACKAGE',		False),
		(r'EXTRACT_PRIV_VIRTUAL',	True),
		(r'EXTRACT_PRIVATE',		False),
		(r'EXTRACT_STATIC',			False),
		(r'FILTER_PATTERNS',		None),
		(r'FORCE_LOCAL_INCLUDES',	False),
		(r'FULL_PATH_NAMES',		True),
		(r'GENERATE_AUTOGEN_DEF',	False),
		(r'GENERATE_BUGLIST',		False),
		(r'GENERATE_CHI',			False),
		(r'GENERATE_DEPRECATEDLIST',False),
		(r'GENERATE_DOCBOOK',		False),
		(r'GENERATE_DOCSET',		False),
		(r'GENERATE_ECLIPSEHELP',	False),
		(r'GENERATE_HTML',			False),
		(r'GENERATE_HTMLHELP',		False),
		(r'GENERATE_LATEX',			False),
		(r'GENERATE_LEGEND',		False),
		(r'GENERATE_MAN',			False),
		(r'GENERATE_PERLMOD',		False),
		(r'GENERATE_QHP',			False),
		(r'GENERATE_RTF',			False),
		(r'GENERATE_SQLITE3',		False),
		(r'GENERATE_TESTLIST',		False),
		(r'GENERATE_TODOLIST',		False),
		(r'GENERATE_TREEVIEW',		False),
		(r'GENERATE_XML',			True),
		(r'HAVE_DOT',				False),
		(r'HIDE_COMPOUND_REFERENCE',False),
		(r'HIDE_FRIEND_COMPOUNDS',	False),
		(r'HIDE_IN_BODY_DOCS',		False),
		(r'HIDE_SCOPE_NAMES',		False),
		(r'HIDE_UNDOC_CLASSES',		True),
		(r'HIDE_UNDOC_MEMBERS',		True),
		(r'HTML_FILE_EXTENSION',	r'.html'),
		(r'HTML_OUTPUT',			r'html'),
		(r'IDL_PROPERTY_SUPPORT',	False),
		(r'INHERIT_DOCS', 			True),
		(r'INLINE_GROUPED_CLASSES',	False),
		(r'INLINE_INFO',			True),
		(r'INLINE_INHERITED_MEMB',	True),
		(r'INLINE_SIMPLE_STRUCTS',	False),
		(r'INLINE_SOURCES',			False),
		(r'INPUT_ENCODING',			r'UTF-8'),
		(r'INPUT_FILTER',			None),
		(r'LOOKUP_CACHE_SIZE',		2),
		(r'MACRO_EXPANSION',		True),
		(r'MARKDOWN_SUPPORT',		True),
		(r'OPTIMIZE_FOR_FORTRAN',	False),
		(r'OPTIMIZE_OUTPUT_FOR_C',	False),
		(r'OPTIMIZE_OUTPUT_JAVA',	False),
		(r'OPTIMIZE_OUTPUT_SLICE',	False),
		(r'OPTIMIZE_OUTPUT_VHDL',	False),
		(r'PYTHON_DOCSTRING', 		True),
		(r'QUIET',					False),
		(r'RECURSIVE',				False),
		(r'REFERENCES_LINK_SOURCE',	False),
		(r'RESOLVE_UNNAMED_PARAMS',	True),
		(r'SEARCH_INCLUDES',		False),
		(r'SEPARATE_MEMBER_PAGES',	False),
		(r'SHORT_NAMES',			False),
		(r'SHOW_GROUPED_MEMB_INC',	False),
		(r'SHOW_USED_FILES',		False),
		(r'SIP_SUPPORT',			False),
		(r'SKIP_FUNCTION_MACROS', 	False),
		(r'SORT_BRIEF_DOCS',		False),
		(r'SORT_BY_SCOPE_NAME',		False),
		(r'SORT_GROUP_NAMES',		True),
		(r'SORT_MEMBER_DOCS',		False),
		(r'SORT_MEMBERS_CTORS_1ST',	True),
		(r'SOURCE_BROWSER',			False),
		(r'STRICT_PROTO_MATCHING',	False),
		(r'SUBGROUPING', 			True),
		(r'TAB_SIZE',				4),
		(r'TYPEDEF_HIDES_STRUCT',	False),
		(r'UML_LOOK',				False),
		(r'USE_HTAGS',				False),
		(r'VERBATIM_HEADERS',		False),
		(r'WARN_IF_DOC_ERROR',		True),
		(r'WARN_IF_INCOMPLETE_DOC',	True),
		(r'WARN_LOGFILE',			None),
		(r'XML_NS_MEMB_FILE_SCOPE',	True),
		(r'XML_OUTPUT',				r'xml'),
		(r'XML_PROGRAMLISTING',		False),
	)

def _preprocess_doxyfile(context):
	assert context is not None
	assert isinstance(context, project.Context)

	with doxygen.Doxyfile(
			doxyfile_path = context.doxyfile_path,
			cwd = context.input_dir,
			logger = context.verbose_logger
		) as df:

		df.append()
		df.append(r'#---------------------------------------------------------------------------')
		df.append(r'# marzer/poxy')
		df.append(r'#---------------------------------------------------------------------------')

		# apply regular doxygen settings
		if 1:
			df.set_value(r'INPUT', context.sources)
			df.set_value(r'FILE_PATTERNS', context.source_patterns)
			df.set_value(r'OUTPUT_DIRECTORY', context.output_dir)
			df.add_value(r'EXCLUDE', context.html_dir)
			df.add_value(r'EXCLUDE', context.xml_dir)

			if not context.name:
				context.name = df.get_value(r'PROJECT_NAME', fallback='')
			df.set_value(r'PROJECT_NAME', context.name)

			if not context.description:
				context.description = df.get_value(r'PROJECT_BRIEF', fallback='')
			df.set_value(r'PROJECT_BRIEF', context.description)

			if context.logo is None:
				context.logo = df.get_value(r'PROJECT_LOGO', fallback=None)
				if context.logo is not None:
					context.logo = Path(str(context.logo))
					if not context.logo.is_absolute():
						context.logo = Path(context.input_dir, context.logo)
					context.logo = context.logo.resolve()
					context.verbose_value(r'Context.logo', context.logo)
			df.set_value(r'PROJECT_LOGO', context.logo)

			if context.show_includes is None:
				context.show_includes = df.get_boolean(r'SHOW_INCLUDE_FILES', fallback=True)
				context.verbose_value(r'Context.show_includes', context.show_includes)
			df.set_value(r'SHOW_INCLUDE_FILES', context.show_includes)

			if context.internal_docs is None:
				context.internal_docs = df.get_boolean(r'INTERNAL_DOCS', fallback=False)
				context.verbose_value(r'Context.internal_docs', context.internal_docs)
			df.set_value(r'INTERNAL_DOCS', context.internal_docs)
			df.add_value(r'ENABLED_SECTIONS', (r'private', r'internal') if context.internal_docs else (r'public', r'external'))

			if context.generate_tagfile is None:
				context.generate_tagfile = not (context.private_repo or context.internal_docs)
				context.verbose_value(r'Context.generate_tagfile', context.generate_tagfile)
			if context.generate_tagfile:
				context.tagfile_path = coerce_path(context.output_dir, rf'{context.name.replace(" ","_")}.tagfile.xml' if context.name else r'tagfile.xml')
				df.set_value(r'GENERATE_TAGFILE', context.tagfile_path.name)
			else:
				df.set_value(r'GENERATE_TAGFILE', None)

			if context.extract_all is None:
				context.extract_all = df.get_boolean(r'EXTRACT_ALL', fallback=False)
				context.verbose_value(r'Context.extract_all', context.extract_all)
			df.set_value(r'EXTRACT_ALL', context.extract_all)

			if context.warnings.enabled is None:
				context.warnings.enabled = df.get_boolean(r'WARNINGS', fallback=True)
				context.verbose_value(r'Context.warnings.enabled', context.warnings.enabled)
			df.set_value(r'WARNINGS', context.warnings.enabled)

			if context.warnings.treat_as_errors is None:
				context.warnings.treat_as_errors = df.get_boolean(r'WARN_AS_ERROR', fallback=False)
				context.verbose_value(r'Context.warnings.treat_as_errors', context.warnings.treat_as_errors)
			df.set_value(r'WARN_AS_ERROR', context.warnings.treat_as_errors)

			if context.warnings.undocumented is None:
				context.warnings.undocumented = df.get_boolean(r'WARN_IF_UNDOCUMENTED', fallback=True)
				context.verbose_value(r'Context.warnings.undocumented', context.warnings.undocumented)
			df.set_value(r'WARN_IF_UNDOCUMENTED', context.warnings.undocumented)

			global _doxygen_overrides
			df.append()
			for k, v in _doxygen_overrides:
				df.set_value(k, v)
			df.set_value(r'NUM_PROC_THREADS', context.threads)
			df.add_value(r'CLANG_OPTIONS', rf'-std=c++{context.cpp%100}')
			df.add_value(r'CLANG_OPTIONS', r'-Wno-everything')
			df.add_value(r'STRIP_FROM_PATH', context.strip_paths)

			if context.tagfiles:
				df.append()
				df.add_value(r'TAGFILES', [rf'{k}={v}' for k,v in context.tagfiles.items()])

			if context.aliases:
				df.append()
				df.add_value(r'ALIASES', [rf'{k}={v}' for k,v in context.aliases.items()])

			if context.defines:
				df.append()
				df.add_value(r'PREDEFINED', [rf'{k}={v}' for k,v in context.defines.items()])

		# apply m.css stuff
		if 1:
			df.append()
			df.append(r'##!')
			df.append(rf'##! M_SHOW_UNDOCUMENTED        = {"YES" if context.extract_all else "NO"}')
			df.append(r'##!')
			if not df.contains(r'M_CLASS_TREE_EXPAND_LEVELS'):
				df.append(r'##! M_CLASS_TREE_EXPAND_LEVELS = 3')
				df.append(r'##!')
			if not df.contains(r'M_FILE_TREE_EXPAND_LEVELS'):
				df.append(r'##! M_FILE_TREE_EXPAND_LEVELS  = 3')
				df.append(r'##!')
			if not df.contains(r'M_EXPAND_INNER_TYPES'):
				df.append(r'##! M_EXPAND_INNER_TYPES       = YES')
				df.append(r'##!')
			if not df.contains(r'M_SEARCH_DOWNLOAD_BINARY'):
				df.append(r'##! M_SEARCH_DOWNLOAD_BINARY   = NO')
				df.append(r'##!')
			if not df.contains(r'M_SEARCH_DISABLED'):
				df.append(r'##! M_SEARCH_DISABLED          = NO')
				df.append(r'##!')
			if not df.contains(r'M_FAVICON'):
				df.append(rf'##! M_FAVICON                  = "{context.favicon if context.favicon is not None else ""}"')
				df.append(r'##!')
			if not df.contains(r'M_LINKS_NAVBAR1') and not df.contains(r'M_LINKS_NAVBAR2'):
				if context.navbar:
					bar = [v for v in context.navbar]
					for i in range(len(bar)):
						if bar[i] == 'github':
							bar[i] = rf'"<a target=\"_blank\" href=\"https://github.com/{context.github}/\" class=\"github\">Github</a>"'
					split = min(max(int(len(bar)/2) + len(bar)%2, 2), len(bar))
					for b, i in ((bar[:split], 1), (bar[split:], 2)):
						if b:
							df.append(rf'##! M_LINKS_NAVBAR{i}            = ''\\')
							for j in range(len(b)):
								df.append(rf'##!     {b[j]}' + (' \\' if j+1 < len(b) else ''))
						else:
							df.append(rf'##! M_LINKS_NAVBAR{i}            = ')
						df.append(r'##!')
				else:
					df.append(r'##! M_LINKS_NAVBAR1            = ')
					df.append(r'##! M_LINKS_NAVBAR2            = ')
					df.append(r'##!')
			if not df.contains(r'M_HTML_HEADER'):
				global _embedded_js
				df.append(r'##! M_HTML_HEADER              = ''\\')
				for k, v in context.meta_tags.items():
					df.append(rf'##!    <meta name="{k}" content="{v}"> ''\\')
				df.append(r'##!    <link href="poxy.css" rel="stylesheet"/> ''\\')
				df.append(rf'##!    <script src="{context.jquery.name}"></script> ''\\')
				df.append(r'##!    <script src="poxy.js"></script>')
				df.append(r'##!')
			if not df.contains(r'M_PAGE_FINE_PRINT'):
				df.append(r'##! M_PAGE_FINE_PRINT          = ''\\')
				top_row = []
				if context.github:
					top_row.append(rf'<a href="https://github.com/{context.github}/">Github</a>')
					top_row.append(rf'<a href="https://github.com/{context.github}/issues">Report an issue</a>')
				if context.generate_tagfile:
					top_row.append(rf'<a href="{context.tagfile_path.name}" target="_blank" type="text/xml" download>Doxygen tagfile</a>')
				if top_row:
					for i in range(len(top_row)):
						df.append(rf'##!     {" &bull; " if i else ""}{top_row[i]} ''\\')
					df.append(r'##!     <br><br> ''\\')
				df.append(r'##!     Documentation created using ''\\')
				df.append(r'##!     <a href="https://www.doxygen.nl/index.html">Doxygen</a> ''\\')
				df.append(r'##!     + <a href="https://mcss.mosra.cz/documentation/doxygen/">mosra/m.css</a> ''\\')
				df.append(r'##!     + <a href="https://github.com/marzer/poxy/">marzer/poxy</a>')
				df.append(r'##!')

		# move to a temp file path
		if context.temp_file_name:
			df.path = coerce_path(context.output_dir, context.temp_file_name)
		else:
			df.path = coerce_path(context.output_dir, df.path.name + rf'.{df.hash()}.temp')
		context.doxyfile_path = df.path
		context.verbose_value(r'Context.doxyfile_path', context.doxyfile_path)

		# debug dump final doxyfile
		df.cleanup()
		if context.dry_run:
			context.info(r'#====================================================================================')
			context.info(r'# poxy-generated Doxyfile')
			context.info(r'#====================================================================================')
			context.info(df.get_text())
			context.info(r'#====================================================================================')
		else:
			context.verbose(r'Effective Doxyfile:')
			context.verbose(df.get_text(), indent='    ')



def _postprocess_xml(context):
	assert context is not None
	assert isinstance(context, project.Context)

	xml_files = get_all_files(context.xml_dir, any=(r'*.xml'))
	if not xml_files:
		return

	with ScopeTimer(rf'Post-processing {len(xml_files)} XML files', print_start=True, print_end=context.verbose_logger):

		pretty_print_xml = False
		xml_parser = etree.XMLParser(
			encoding='utf-8',
			remove_blank_text=pretty_print_xml,
			recover=True,
			remove_comments=True,
			ns_clean=True
		)
		write_xml_to_file = lambda xml, f: xml.write(str(f), encoding='utf-8', xml_declaration=True, pretty_print=pretty_print_xml)

		inline_namespace_ids = None
		if context.inline_namespaces:
			inline_namespace_ids = [f'namespace{doxygen.mangle_name(ns)}' for ns in context.inline_namespaces]

		implementation_header_data = None
		implementation_header_mappings = None
		implementation_header_innernamespaces = None
		implementation_header_sectiondefs = None
		if context.implementation_headers:
			implementation_header_data = [
				(
					hp,
					os.path.basename(hp),
					doxygen.mangle_name(os.path.basename(hp)),
					[(i, os.path.basename(i), doxygen.mangle_name(os.path.basename(i))) for i in impl]
				)
				for hp, impl in context.implementation_headers
			]
			implementation_header_mappings = dict()
			implementation_header_innernamespaces = dict()
			implementation_header_sectiondefs = dict()
			for hdata in implementation_header_data:
				implementation_header_innernamespaces[hdata[2]] = []
				implementation_header_sectiondefs[hdata[2]] = []
				for (ip, ifn, iid) in hdata[3]:
					implementation_header_mappings[iid] = hdata

		if 1:

			# pre-pass to delete file and dir entries where appropriate:
			if 1:
				dox_files = (r'dox', r'md')
				dox_files = [rf'*_8{ext}.xml' for ext in dox_files]
				for xml_file in get_all_files(context.xml_dir, any=dox_files):
					delete_file(xml_file, logger=context.verbose_logger)
				deleted = True
				while deleted:
					deleted = False
					for xml_file in get_all_files(context.xml_dir, all=(r'dir_*.xml')):
						xml = etree.parse(str(xml_file), parser=xml_parser)
						compounddef = xml.getroot().find(r'compounddef')
						if compounddef is None or compounddef.get(r'kind') != r'dir':
							continue
						existing_inners = 0
						for subtype in (r'innerfile', r'innerdir'):
							for inner in compounddef.findall(subtype):
								ref_file = Path(context.xml_dir, rf'{inner.get(r"refid")}.xml')
								if ref_file.exists():
									existing_inners = existing_inners + 1
						if not existing_inners:
							delete_file(xml_file, logger=context.verbose_logger)
							deleted = True

			extracted_implementation = False
			tentative_macros = regex_or(context.highlighting.macros)
			macros = set()
			cpp_tree = CppTree()
			xml_files = get_all_files(context.xml_dir, any=(r'*.xml'))
			for xml_file in xml_files:
				context.verbose(rf'Pre-processing {xml_file}')
				xml = etree.parse(str(xml_file), parser=xml_parser)
				root = xml.getroot()
				changed = False

				# the doxygen index
				if root.tag == r'doxygenindex':

					# remove entries for files we might have explicitly deleted above
					for compound in [tag for tag in root.findall(r'compound') if tag.get(r'kind') in (r'file', r'dir')]:
						ref_file = Path(context.xml_dir, rf'{compound.get(r"refid")}.xml')
						if not ref_file.exists():
							root.remove(compound)
							changed = True

					# extract namespaces, types and enum values for syntax highlighting
					scopes = [tag for tag in root.findall(r'compound') if tag.get(r'kind') in (r'namespace', r'class', r'struct', r'union')]
					for scope in scopes:
						scope_name = scope.find(r'name').text

						# skip template members because they'll break the regex matchers
						if scope_name.find(r'<') != -1:
							continue

						# regular types and namespaces
						if scope.get(r'kind') in (r'class', r'struct', r'union'):
							cpp_tree.add_type(scope_name)
						elif scope.get(r'kind') == r'namespace':
							cpp_tree.add_namespace(scope_name)

						# nested enums
						enum_tags = [tag for tag in scope.findall(r'member') if tag.get(r'kind') in (r'enum', r'enumvalue')]
						enum_name = ''
						for tag in enum_tags:
							if tag.get(r'kind') == r'enum':
								enum_name = rf'{scope_name}::{tag.find("name").text}'
								cpp_tree.add_type(enum_name)
							else:
								assert enum_name
								cpp_tree.add_enum_value(rf'{enum_name}::{tag.find("name").text}')

						# nested typedefs
						typedefs = [tag for tag in scope.findall(r'member') if tag.get(r'kind') == r'typedef']
						for typedef in typedefs:
							cpp_tree.add_type(rf'{scope_name}::{typedef.find("name").text}')

				# some other compound definition
				else:
					compounddef = root.find(r'compounddef')
					assert compounddef is not None
					compoundname = compounddef.find(r'compoundname')
					assert compoundname is not None
					assert compoundname.text

					if compounddef.get(r'kind') in (r'namespace', r'class', r'struct', r'union', r'enum', r'file', r'group'):

						# merge user-defined sections with the same name
						sectiondefs = [s for s in compounddef.findall(r'sectiondef') if s.get(r'kind') == r'user-defined']
						sections = dict()
						for section in sectiondefs:
							header = section.find(r'header')
							if header is not None and header.text:
								if header.text not in sections:
									sections[header.text] = []
							sections[header.text].append(section)
						for key, vals in sections.items():
							if len(vals) > 1:
								first_section = vals.pop(0)
								for section in vals:
									for member in section.findall(r'memberdef'):
										section.remove(member)
										first_section.append(member)
									compounddef.remove(section)
									changed = True

						# sort user-defined sections based on their name
						sectiondefs = [s for s in compounddef.findall(r'sectiondef') if s.get(r'kind') == r'user-defined']
						sectiondefs = [s for s in sectiondefs if s.find(r'header') is not None]
						for section in sectiondefs:
							compounddef.remove(section)
						sectiondefs.sort(key=lambda s: s.find(r'header').text)
						for section in sectiondefs:
							compounddef.append(section)
							changed = True

						# per-section stuff
						for section in compounddef.findall(r'sectiondef'):

							# remove members which are listed multiple times because doxygen is idiotic:
							members = [tag for tag in section.findall(r'memberdef')]
							for i in range(len(members)-1, 0, -1):
								for j in range(i):
									if members[i].get(r'id') == members[j].get(r'id'):
										section.remove(members[i])
										changed = True
										break

							# re-sort members to override Doxygen's weird and stupid sorting 'rules'
							if 1:
								sort_members_by_name = lambda tag: tag.find(r'name').text
								members = [tag for tag in section.findall(r'memberdef')]
								for tag in members:
									section.remove(tag)
								groups = [
									([tag for tag in members if tag.get(r'kind') == r'define'], True),
									([tag for tag in members if tag.get(r'kind') == r'typedef'], True),
									([tag for tag in members if tag.get(r'kind') == r'enum'], True),
									([tag for tag in members if tag.get(r'kind') == r'variable' and tag.get(r'static') == r'yes'], True),
									(
										[tag for tag in members if tag.get(r'kind') == r'variable' and tag.get(r'static') == r'no'],
										compounddef.get(r'kind') not in (r'class', r'struct', r'union')
									),
									([tag for tag in members if tag.get(r'kind') == r'function' and tag.get(r'static') == r'yes'], True),
									([tag for tag in members if tag.get(r'kind') == r'function' and tag.get(r'static') == r'no'], True),
									([tag for tag in members if tag.get(r'kind') == r'friend'], True)
								]
								for group, sort in groups:
									if sort:
										group.sort(key=sort_members_by_name)
									for tag in group:
										members.remove(tag)
										section.append(tag)
										changed = True
								# if we've missed any groups just glob them on the end
								if members:
									members.sort(key=sort_members_by_name)
									changed = True
									for tag in members:
										section.append(tag)

					# namespaces
					if compounddef.get(r'kind') == r'namespace':

						# set inline namespaces
						if context.inline_namespaces:
							for nsid in inline_namespace_ids:
								if compounddef.get(r'id') == nsid:
									compounddef.set(r'inline', r'yes')
									changed = True
									break

					# dirs
					if compounddef.get(r'kind') == r'dir':

						# remove implementation headers
						if context.implementation_headers:
							for innerfile in compounddef.findall(r'innerfile'):
								if innerfile.get(r'refid') in implementation_header_mappings:
									compounddef.remove(innerfile)
									changed = True

					# files
					if compounddef.get(r'kind') == r'file':

						# simplify the XML by removing unnecessary junk
						for tag in (r'includes', r'includedby', r'incdepgraph', r'invincdepgraph'):
							tags = compounddef.findall(tag)
							if tags:
								for t in tags:
									compounddef.remove(t)
									changed = True

						# get any macros for the syntax highlighter
						define_sections = [tag for tag in compounddef.findall(r'sectiondef') if tag.get(r'kind') == r'define']
						for define_section in define_sections:
							defines = [tag for tag in define_section.findall(r'memberdef') if tag.get(r'kind') == r'define']
							for define in defines:
								# if (define.find('briefdescription').text.strip()
								# 		or define.find('detaileddescription').text.strip()
								# 		or define.find('inbodydescription').text.strip()):
								macro = define.find(r'name').text
								if not tentative_macros.fullmatch(macro):
									macros.add(macro)

						# rip the good bits out of implementation headers
						if context.implementation_headers:
							if compounddef.get(r'id') in implementation_header_mappings:
								hid = implementation_header_mappings[compounddef.get("id")][2]
								innernamespaces = compounddef.findall(r'innernamespace')
								if innernamespaces:
									implementation_header_innernamespaces[hid] = implementation_header_innernamespaces[hid] + innernamespaces
									extracted_implementation = True
									for tag in innernamespaces:
										compounddef.remove(tag)
										changed = True
								sectiondefs = compounddef.findall(r'sectiondef')
								if sectiondefs:
									implementation_header_sectiondefs[hid] = implementation_header_sectiondefs[hid] + sectiondefs
									extracted_implementation = True
									for tag in sectiondefs:
										compounddef.remove(tag)
										changed = True

				if changed:
					write_xml_to_file(xml, xml_file)

			# add to syntax highlighter
			context.highlighting.namespaces.add(cpp_tree.matcher(CppTree.NAMESPACES))
			context.highlighting.types.add(cpp_tree.matcher(CppTree.TYPES))
			context.highlighting.enums.add(cpp_tree.matcher(CppTree.ENUM_VALUES))
			for macro in macros:
				context.highlighting.macros.add(macro)

			# merge extracted implementations
			if extracted_implementation:
				for (hp, hfn, hid, impl) in implementation_header_data:
					xml_file = coerce_path(context.xml_dir, rf'{hid}.xml')
					context.verbose(rf'Merging implementation nodes into {xml_file}')
					xml = etree.parse(str(xml_file), parser=xml_parser)
					compounddef = xml.getroot().find(r'compounddef')
					changed = False

					innernamespaces = compounddef.findall(r'innernamespace')
					for new_tag in implementation_header_innernamespaces[hid]:
						matched = False
						for existing_tag in innernamespaces:
							if existing_tag.get(r'refid') == new_tag.get(r'refid'):
								matched = True
								break
						if not matched:
							compounddef.append(new_tag)
							innernamespaces.append(new_tag)
							changed = True

					sectiondefs = compounddef.findall(r'sectiondef')
					for new_section in implementation_header_sectiondefs[hid]:
						matched_section = False
						for existing_section in sectiondefs:
							if existing_section.get(r'kind') == new_section.get(r'kind'):
								matched_section = True

								memberdefs = existing_section.findall(r'memberdef')
								new_memberdefs = new_section.findall(r'memberdef')
								for new_memberdef in new_memberdefs:
									matched = False
									for existing_memberdef in memberdefs:
										if existing_memberdef.get(r'id') == new_memberdef.get(r'id'):
											matched = True
											break

									if not matched:
										new_section.remove(new_memberdef)
										existing_section.append(new_memberdef)
										memberdefs.append(new_memberdef)
										changed = True
								break

						if not matched_section:
							compounddef.append(new_section)
							sectiondefs.append(new_section)
							changed = True

					if changed:
						write_xml_to_file(xml, xml_file)

		# delete the impl header xml files
		if 1 and context.implementation_headers:
			for hdata in implementation_header_data:
				for (ip, ifn, iid) in hdata[3]:
					delete_file(coerce_path(context.xml_dir, rf'{iid}.xml'), logger=context.verbose_logger)

		# scan through the files and substitute impl header ids and paths as appropriate
		if 1 and context.implementation_headers:
			xml_files = get_all_files(context.xml_dir, any=('*.xml'))
			for xml_file in xml_files:
				context.verbose(rf"Re-linking implementation headers in '{xml_file}'")
				xml_text = read_all_text_from_file(xml_file, logger=context.verbose_logger)
				for (hp, hfn, hid, impl) in implementation_header_data:
					for (ip, ifn, iid) in impl:
						#xml_text = xml_text.replace(f'refid="{iid}"',f'refid="{hid}"')
						xml_text = xml_text.replace(rf'compoundref="{iid}"',f'compoundref="{hid}"')
						xml_text = xml_text.replace(ip,hp)
				with BytesIO(bytes(xml_text, 'utf-8')) as b:
					xml = etree.parse(b, parser=xml_parser)
					write_xml_to_file(xml, xml_file)



_worker_context = None
def _initialize_worker(context):
	global _worker_context
	_worker_context = context



def _postprocess_html_file(path, context=None):
	assert path is not None
	assert isinstance(path, Path)
	assert path.is_absolute()
	assert path.exists()

	if context is None:
		global _worker_context
		context = _worker_context
	assert context is not None
	assert isinstance(context, project.Context)

	context.verbose(rf'Post-processing {path}')
	changed = False
	doc = soup.HTMLDocument(path, logger=context.verbose_logger)
	for fix in context.fixers:
		if fix(doc, context):
			doc.smooth()
			changed = True
	if changed:
		doc.flush()
	return changed



def _postprocess_html(context):
	assert context is not None
	assert isinstance(context, project.Context)

	files = get_all_files(context.html_dir, any=('*.html', '*.htm'))
	if not files:
		return

	threads = min(len(files), context.threads, 4)

	with ScopeTimer(rf'Post-processing {len(files)} HTML files', print_start=True, print_end=context.verbose_logger):
		context.fixers = (
			fixers.CodeBlocks()
			, fixers.IndexPage()
			, fixers.Modifiers1()
			, fixers.Modifiers2()
			, fixers.TemplateTemplate()
			, fixers.StripIncludes()
			, fixers.AutoDocLinks()
			, fixers.Links()
			, fixers.CustomTags()
			, fixers.EmptyTags()
		)
		context.verbose(rf'Post-processing {len(files)} HTML files...')
		if threads > 1:
			with futures.ProcessPoolExecutor(max_workers=threads, initializer=_initialize_worker, initargs=(context,)) as executor:
				jobs = [ executor.submit(_postprocess_html_file, file) for file in files ]
				for future in futures.as_completed(jobs):
					try:
						future.result()
					except:
						try:
							executor.shutdown(wait=False, cancel_futures=True)
						except TypeError:
							executor.shutdown(wait=False)
						raise

		else:
			for file in files:
				_postprocess_html_file(file, context)



#=======================================================================================================================
# RUN
#=======================================================================================================================

def run(config_path='.', output_dir='.', threads=-1, cleanup=True, verbose=False, mcss_dir=None, temp_file_name=None, logger=None, dry_run=False):

	context = project.Context(
		config_path = config_path,
		output_dir = output_dir,
		threads = threads,
		cleanup = cleanup,
		verbose = verbose,
		mcss_dir = mcss_dir,
		temp_file_name = temp_file_name,
		logger = logger,
		dry_run = dry_run
	)

	with ScopeTimer(r'All tasks', print_start=False, print_end=context.verbose if dry_run else context.info) as all_tasks_timer:

		# preprocess the doxyfile
		_preprocess_doxyfile(context)
		context.verbose_object(r'Context.warnings', context.warnings)

		# preprocessing the doxyfile creates a temp copy; this is the cleanup block.
		try:
			if not dry_run:

				# delete any leftovers from the previous run
				if 1:
					delete_directory(context.xml_dir, logger=context.verbose_logger)
					delete_directory(context.html_dir, logger=context.verbose_logger)

				# run doxygen to generate the xml
				if 1:
					with ScopeTimer(r'Generating XML files with Doxygen', print_start=True, print_end=context.verbose_logger) as t:
						with tempfile.SpooledTemporaryFile(mode='w+', newline='\n', encoding='utf-8') as file:
							try:
								subprocess.run(
									['doxygen', str(context.doxyfile_path)],
									check=True,
									stdout=file,
									stderr=file,
									cwd=context.input_dir
								)
							except:
								context.warning(r'Doxygen failed! Output dump:')
								file.seek(0)
								context.info(file.read(), indent=r'    ')
								raise
							context.verbose(r'Doxygen output dump:')
							file.seek(0)
							context.verbose(file.read(), indent=r'    ')

						# remove the local paths from the tagfile since they're meaningless (and a privacy breach)
						if context.tagfile_path is not None and context.tagfile_path.exists():
							text = read_all_text_from_file(context.tagfile_path, logger=context.verbose_logger)
							text = re.sub(r'\n\s*?<path>.+?</path>\s*?\n', '\n', text, re.S)
							with open(context.tagfile_path, 'w', encoding='utf-8', newline='\n') as f:
								f.write(text)

				# post-process xml files
				if 1:
					_postprocess_xml(context)

				context.verbose_object(r'Context.highlighting', context.highlighting)

				# compile regexes
				# (done here because doxygen and xml preprocessing adds additional values to these lists)
				context.highlighting.namespaces = regex_or(context.highlighting.namespaces, pattern_prefix='(?:::)?', pattern_suffix='(?:::)?')
				context.highlighting.types = regex_or(context.highlighting.types, pattern_prefix='(?:::)?', pattern_suffix='(?:::)?')
				context.highlighting.enums = regex_or(context.highlighting.enums, pattern_prefix='(?:::)?')
				context.highlighting.string_literals = regex_or(context.highlighting.string_literals)
				context.highlighting.numeric_literals = regex_or(context.highlighting.numeric_literals)
				context.highlighting.macros = regex_or(context.highlighting.macros)
				context.autolinks = tuple([(re.compile('(?<![a-zA-Z_])' + expr + '(?![a-zA-Z_])'), uri) for expr, uri in context.autolinks])

				# run m.css to generate the html
				if 1:
					with ScopeTimer(r'Generating HTML files with m.css', print_start=True, print_end=context.verbose_logger) as t:
						with tempfile.SpooledTemporaryFile(mode='w+', newline='\n', encoding='utf-8') as file:
							doxy_args = [str(context.doxyfile_path), r'--no-doxygen', r'--sort-globbed-files']
							if context.is_verbose():
								doxy_args.append(r'--debug')
							try:
								run_python_script(
									coerce_path(context.mcss_dir, r'documentation/doxygen.py'),
									*doxy_args,
									stdout=file,
									stderr=file,
									cwd=context.input_dir
								)
							except:
								context.warning(r'm.css failed! Output dump:')
								file.seek(0)
								context.info(file.read(), indent=r'    ')
								raise
							context.verbose(r'm.css output dump:')
							file.seek(0)
							context.verbose(file.read(), indent=r'    ')

				# copy extra_files
				with ScopeTimer(r'Copying extra_files', print_start=True, print_end=context.verbose_logger) as t:
					for f in context.extra_files:
						copy_file(f, coerce_path(context.html_dir, f.name), logger=context.verbose_logger)

				# delete the xml
				if context.cleanup:
					delete_directory(context.xml_dir, logger=context.logger)

				# move the tagfile into the html directory
				if context.generate_tagfile:
					if context.tagfile_path.exists():
						move_file(context.tagfile_path, coerce_path(context.output_dir, 'html'), logger=context.verbose_logger)
					else:
						context.warning(rf'Doxygen tagfile {context.tagfile_path} not found!')

				# post-process html files
				if 1:
					_postprocess_html(context)

		# delete the temp doxyfile
		finally:
			if context.cleanup:
				delete_file(context.doxyfile_path, logger=context.verbose_logger)



def main():
	verbose = False
	try:
		args = argparse.ArgumentParser(
			description=r'Generate fancy C++ documentation.',
			formatter_class=argparse.RawTextHelpFormatter
		)
		args.add_argument(
			r'config',
			type=Path,
			nargs='?',
			default=Path('.'),
			help=r'a path to a Doxyfile, poxy.toml, or a directory containing one/both (default: %(default)s/)'
		)
		args.add_argument(
			 r'-v', r'--verbose',
			action=r'store_true',
			help=r"enables very noisy diagnostic output"
		)
		args.add_argument(
			r'--dry',
			action=r'store_true',
			help=r"does a 'dry run' only, stopping after emitting the effective Doxyfile"
		)
		args.add_argument(
			r'--threads',
			type=int,
			default=0,
			metavar=r'<N>',
			help=r"sets the number of threads used (default: automatic)"
		)
		args.add_argument(
			r'--m.css',
			type=Path,
			default=None,
			metavar=r'<path>',
			help=r"overrides the version of m.css used for documentation generation",
			dest=r'mcss'
		)
		args.add_argument(r'--nocleanup', action=r'store_true', help=argparse.SUPPRESS)
		args.add_argument(r'--temp_file_name', type=str, default=None, metavar=r'<file name>', help=argparse.SUPPRESS)
		args = args.parse_args()
		verbose = args.verbose
		result = run(
			config_path = args.config,
			output_dir = Path.cwd(),
			threads = args.threads,
			cleanup = not args.nocleanup,
			verbose = verbose,
			mcss_dir = args.mcss,
			temp_file_name = args.temp_file_name,
			logger=True, # stderr + stdout
			dry_run=args.dry
		)
		if result is None or bool(result):
			sys.exit(0)
		else:
			sys.exit(1)
	except Exception as err:
		print_exception(err, include_type=verbose, include_traceback=verbose, skip_frames=1)
		sys.exit(-1)



if __name__ == '__main__':
	main()
