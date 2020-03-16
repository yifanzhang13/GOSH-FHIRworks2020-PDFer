using HDR_UK_Web_Application.IServices;
using Newtonsoft.Json.Linq;
using System.Collections.Generic;
using System.Threading.Tasks;
using System;
using System.Diagnostics;
using System.ComponentModel;
using System.IO;

namespace HDR_UK_Web_Application.Services
{
    public class PatientService : IPatientService
    {
        private static readonly string requestOption = "/Patient/";
        private readonly IResourceFetchService _resource;
        private readonly ILoggerManager _logger;

        public PatientService(IResourceFetchService resource, ILoggerManager logger)
        {
            _resource = resource;
            _logger = logger;
        }

        public async Task<List<JObject>> GetPatients()
        {
            _logger.LogInfo("Class: PatientService, Method: GetAllPages");
            List<JObject> patients = await _resource.GetAllPages(requestOption);
            return patients;
        }

        public async Task<List<JObject>> GetPatientPages(int pages)
        {
            _logger.LogInfo("Class: PatientService, Method: GetPatientPages");
            return await _resource.GetPages(requestOption, pages);
        }

        public async Task<JObject> GetPatient(string id)
        {
            _logger.LogInfo("Class: PatientService, Method: GetPatient");
            JObject jObject = await _resource.GetSinglePage($"{requestOption}{id}");

            Process process = new Process() {
                StartInfo = new ProcessStartInfo{
                    FileName = "python3",
                    Arguments = "id.py",
                    WorkingDirectory = Directory.GetCurrentDirectory(),
                    RedirectStandardInput = true
                }
            };

            process.Start();
            process.StandardInput.WriteLine(jObject.ToString());
            process.StandardInput.Close();
            return jObject;
        }
    }
}